#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:21:18 2022

@author: farid
"""
import numpy as np
from scipy import stats, signal, linalg, sparse
from scipy.spatial import distance
from copy import deepcopy, copy
from tqdm import tqdm
import scipy.optimize as opt
from sklearn.metrics import mean_squared_error
import multiprocessing
import matplotlib.pyplot as plt
import sys
import os
import gc
import seaborn as sns
from joblib import Parallel, delayed
import resource
from .exploration import Exploration


class SeqDesign():
    """ Sequential experimental design
    This class provieds method for trainig the meta-model in an iterative
    manners.
    The main method to execute the task is `train_seq_design`, which
      recieves a model object and returns the trained metamodel.
    """

    # -------------------------------------------------------------------------
    def train_seq_design(self, MetaModel):
        """
        Starts the adaptive sequential design for refining the surrogate model
        by selecting training points in a sequential manner.

        Parameters
        ----------
        Model : object
            An object containing all model specifications.

        Returns
        -------
        MetaModel : object
            Meta model object.

        """
        # MetaModel = self
        Model = MetaModel.ModelObj
        self.MetaModel = MetaModel
        self.Model = Model

        # Initialization
        MetaModel.SeqModifiedLOO = {}
        MetaModel.seqValidError = {}
        MetaModel.SeqBME = {}
        MetaModel.SeqKLD = {}
        MetaModel.SeqDistHellinger = {}
        MetaModel.seqRMSEMean = {}
        MetaModel.seqRMSEStd = {}
        MetaModel.seqMinDist = []
        pce = True if MetaModel.meta_model_type.lower() != 'gpe' else False
        mc_ref = True if bool(Model.mc_reference) else False
        if mc_ref:
            Model.read_mc_reference()

        if not hasattr(MetaModel, 'valid_likelihoods'):
            MetaModel.valid_samples = []
            MetaModel.valid_model_runs = []
            MetaModel.valid_likelihoods = []

        # Get the parameters
        max_n_samples = MetaModel.ExpDesign.n_max_samples
        mod_LOO_threshold = MetaModel.ExpDesign.mod_LOO_threshold
        n_canddidate = MetaModel.ExpDesign.n_canddidate
        post_snapshot = MetaModel.ExpDesign.post_snapshot
        n_replication = MetaModel.ExpDesign.n_replication
        util_func = MetaModel.ExpDesign.util_func
        output_name = Model.Output.names
        validError = None
        # Handle if only one UtilityFunctions is provided
        if not isinstance(util_func, list):
            util_func = [MetaModel.ExpDesign.util_func]

        # Read observations or MCReference
        if len(Model.observations) != 0 or Model.meas_file is not None:
            self.observations = Model.read_observation()
            obs_data = self.observations
        else:
            obs_data = []
            TotalSigma2 = {}
        # ---------- Initial MetaModel ----------
        initMetaModel = deepcopy(MetaModel)

        # Validation error if validation set is provided.
        if len(MetaModel.valid_model_runs) != 0:
            init_rmse, init_valid_error = self.__validError(initMetaModel)
            init_valid_error = list(init_valid_error.values())
        else:
            init_rmse = None

        # Check if discrepancy is provided
        if len(obs_data) != 0 and hasattr(MetaModel, 'Discrepancy'):
            TotalSigma2 = MetaModel.Discrepancy.parameters

            # Calculate the initial BME
            out = self.__BME_Calculator(
                initMetaModel, obs_data, TotalSigma2, init_rmse)
            init_BME, init_KLD, init_post, init_likes, init_dist_hellinger = out
            print(f"\nInitial BME: {init_BME:.2f}")
            print(f"Initial KLD: {init_KLD:.2f}")

            # Posterior snapshot (initial)
            if post_snapshot:
                parNames = MetaModel.ExpDesign.par_names
                print('Posterior snapshot (initial) is being plotted...')
                self.__posteriorPlot(init_post, parNames, 'SeqPosterior_init')

        # Check the convergence of the Mean & Std
        if mc_ref and pce:
            init_rmse_mean, init_rmse_std = self.__error_Mean_Std()
            print(f"Initial Mean and Std error: {init_rmse_mean},"
                  f" {init_rmse_std}")

        # Read the initial experimental design
        Xinit = initMetaModel.ExpDesign.X
        init_n_samples = len(MetaModel.ExpDesign.X)
        initYprev = initMetaModel.ModelOutputDict
        initLCerror = initMetaModel.LCerror
        n_itrs = max_n_samples - init_n_samples

        # Read the initial ModifiedLOO
        if pce:
            Scores_all, varExpDesignY = [], []
            for out_name in output_name:
                y = initMetaModel.ExpDesign.Y[out_name]
                Scores_all.append(list(
                    initMetaModel.score_dict['b_1'][out_name].values()))
                if MetaModel.dim_red_method.lower() == 'pca':
                    pca = MetaModel.pca['b_1'][out_name]
                    components = pca.transform(y)
                    varExpDesignY.append(np.var(components, axis=0))
                else:
                    varExpDesignY.append(np.var(y, axis=0))

            Scores = [item for sublist in Scores_all for item in sublist]
            weights = [item for sublist in varExpDesignY for item in sublist]
            init_mod_LOO = [np.average([1-score for score in Scores],
                                       weights=weights)]

        prevMetaModel_dict = {}
        # Replicate the sequential design
        for repIdx in range(n_replication):
            print(f'\n>>>> Replication: {repIdx+1}<<<<')

            # To avoid changes ub original aPCE object
            MetaModel.ExpDesign.X = Xinit
            MetaModel.ExpDesign.Y = initYprev
            MetaModel.LCerror = initLCerror

            for util_f in util_func:
                print(f'\n>>>> Utility Function: {util_f} <<<<')
                # To avoid changes ub original aPCE object
                MetaModel.ExpDesign.X = Xinit
                MetaModel.ExpDesign.Y = initYprev
                MetaModel.LCerror = initLCerror

                # Set the experimental design
                Xprev = Xinit
                total_n_samples = init_n_samples
                Yprev = initYprev

                Xfull = []
                Yfull = []

                # Store the initial ModifiedLOO
                if pce:
                    print("\nInitial ModifiedLOO:", init_mod_LOO)
                    SeqModifiedLOO = np.array(init_mod_LOO)

                if len(MetaModel.valid_model_runs) != 0:
                    SeqValidError = np.array(init_valid_error)

                # Check if data is provided
                if len(obs_data) != 0:
                    SeqBME = np.array([init_BME])
                    SeqKLD = np.array([init_KLD])
                    SeqDistHellinger = np.array([init_dist_hellinger])

                if mc_ref and pce:
                    seqRMSEMean = np.array([init_rmse_mean])
                    seqRMSEStd = np.array([init_rmse_std])

                # ------- Start Sequential Experimental Design -------
                postcnt = 1
                for itr_no in range(1, n_itrs+1):
                    print(f'\n>>>> Iteration number {itr_no} <<<<')

                    # Save the metamodel prediction before updating
                    prevMetaModel_dict[itr_no] = deepcopy(MetaModel)
                    if itr_no > 1:
                        pc_model = prevMetaModel_dict[itr_no-1]
                        self._y_hat_prev, _ = pc_model.eval_metamodel(
                            samples=Xfull[-1].reshape(1, -1))

                    # Optimal Bayesian Design
                    m_1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
                    MetaModel.ExpDesignFlag = 'sequential'
                    Xnew, updatedPrior = self.opt_SeqDesign(TotalSigma2,
                                                            n_canddidate,
                                                            util_f)
                    m_2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
                    S = np.min(distance.cdist(Xinit, Xnew, 'euclidean'))
                    MetaModel.seqMinDist.append(S)
                    print(f"\nmin Dist from OldExpDesign: {S:2f}")
                    print("\n")

                    # Evaluate the full model response at the new sample
                    Ynew, _ = Model.run_model_parallel(
                        Xnew, prevRun_No=total_n_samples
                        )
                    total_n_samples += Xnew.shape[0]
                    # ------ Plot the surrogate model vs Origninal Model ------
                    if hasattr(MetaModel, 'adapt_verbose') and \
                       MetaModel.adapt_verbose:
                        from .adaptPlot import adaptPlot
                        y_hat, std_hat = MetaModel.eval_metamodel(samples=Xnew)
                        adaptPlot(MetaModel, Ynew, y_hat, std_hat, plotED=False)

                    # -------- Retrain the surrogate model -------
                    # Extend new experimental design
                    Xfull = np.vstack((Xprev, Xnew))

                    # Updating experimental design Y
                    for out_name in output_name:
                        Yfull = np.vstack((Yprev[out_name], Ynew[out_name]))
                        MetaModel.ModelOutputDict[out_name] = Yfull

                    # Pass new design to the metamodel object
                    MetaModel.ExpDesign.sampling_method = 'user'
                    MetaModel.ExpDesign.X = Xfull
                    MetaModel.ExpDesign.Y = MetaModel.ModelOutputDict

                    # Save the Experimental Design for next iteration
                    Xprev = Xfull
                    Yprev = MetaModel.ModelOutputDict

                    # Pass the new prior as the input
                    MetaModel.input_obj.poly_coeffs_flag = False
                    if updatedPrior is not None:
                        MetaModel.input_obj.poly_coeffs_flag = True
                        print("updatedPrior:", updatedPrior.shape)
                        # Arbitrary polynomial chaos
                        for i in range(updatedPrior.shape[1]):
                            MetaModel.input_obj.Marginals[i].dist_type = None
                            x = updatedPrior[:, i]
                            MetaModel.input_obj.Marginals[i].raw_data = x

                    # Train the surrogate model for new ExpDesign
                    MetaModel.train_norm_design(parallel=False)
                    m_3 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024

                    # -------- Evaluate the retrained surrogate model -------
                    # Extract Modified LOO from Output
                    if pce:
                        Scores_all, varExpDesignY = [], []
                        for out_name in output_name:
                            y = MetaModel.ExpDesign.Y[out_name]
                            Scores_all.append(list(
                                MetaModel.score_dict['b_1'][out_name].values()))
                            if MetaModel.dim_red_method.lower() == 'pca':
                                pca = MetaModel.pca['b_1'][out_name]
                                components = pca.transform(y)
                                varExpDesignY.append(np.var(components,
                                                            axis=0))
                            else:
                                varExpDesignY.append(np.var(y, axis=0))
                        Scores = [item for sublist in Scores_all for item
                                  in sublist]
                        weights = [item for sublist in varExpDesignY for item
                                   in sublist]
                        ModifiedLOO = [np.average(
                            [1-score for score in Scores], weights=weights)]

                        print('\n')
                        print(f"Updated ModifiedLOO {util_f}:\n", ModifiedLOO)
                        print('\n')

                    # Compute the validation error
                    if len(MetaModel.valid_model_runs) != 0:
                        rmse, validError = self.__validError(MetaModel)
                        ValidError = list(validError.values())
                    else:
                        rmse = None

                    # Store updated ModifiedLOO
                    if pce:
                        SeqModifiedLOO = np.vstack(
                            (SeqModifiedLOO, ModifiedLOO))
                        if len(MetaModel.valid_model_runs) != 0:
                            SeqValidError = np.vstack(
                                (SeqValidError, ValidError))
                    m_4 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
                    # -------- Caclulation of BME as accuracy metric -------
                    # Check if data is provided
                    if len(obs_data) != 0:
                        # Calculate the initial BME
                        out = self.__BME_Calculator(MetaModel, obs_data,
                                                    TotalSigma2, rmse)
                        BME, KLD, Posterior, likes, DistHellinger = out
                        print('\n')
                        print(f"Updated BME: {BME:.2f}")
                        print(f"Updated KLD: {KLD:.2f}")
                        print('\n')

                        # Plot some snapshots of the posterior
                        step_snapshot = MetaModel.ExpDesign.step_snapshot
                        if post_snapshot and postcnt % step_snapshot == 0:
                            parNames = MetaModel.ExpDesign.par_names
                            print('Posterior snapshot is being plotted...')
                            self.__posteriorPlot(Posterior, parNames,
                                                 f'SeqPosterior_{postcnt}')
                        postcnt += 1
                    m_5 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024

                    # Check the convergence of the Mean&Std
                    if mc_ref and pce:
                        print('\n')
                        RMSE_Mean, RMSE_std = self.__error_Mean_Std()
                        print(f"Updated Mean and Std error: {RMSE_Mean:.2f}, "
                              f"{RMSE_std:.2f}")
                        print('\n')

                    # Store the updated BME & KLD
                    # Check if data is provided
                    if len(obs_data) != 0:
                        SeqBME = np.vstack((SeqBME, BME))
                        SeqKLD = np.vstack((SeqKLD, KLD))
                        SeqDistHellinger = np.vstack((SeqDistHellinger,
                                                      DistHellinger))
                    if mc_ref and pce:
                        seqRMSEMean = np.vstack((seqRMSEMean, RMSE_Mean))
                        seqRMSEStd = np.vstack((seqRMSEStd, RMSE_std))

                    if pce and any(LOO < mod_LOO_threshold
                                   for LOO in ModifiedLOO):
                        break

                    print(f"Memory itr {itr_no}: I: {m_2-m_1:.2f} MB")
                    print(f"Memory itr {itr_no}: II: {m_3-m_2:.2f} MB")
                    print(f"Memory itr {itr_no}: III: {m_4-m_3:.2f} MB")
                    print(f"Memory itr {itr_no}: IV: {m_5-m_4:.2f} MB")
                    m_6 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
                    print(f"Memory itr {itr_no}: total: {m_6:.2f} MB")

                    # Clean up
                    if len(obs_data) != 0:
                        del out
                    gc.collect()
                    print()
                    print('-'*50)
                    print()

                # Store updated ModifiedLOO and BME in dictonary
                strKey = f'{util_f}_rep_{repIdx+1}'
                if pce:
                    MetaModel.SeqModifiedLOO[strKey] = SeqModifiedLOO
                if len(MetaModel.valid_model_runs) != 0:
                    MetaModel.seqValidError[strKey] = SeqValidError

                # Check if data is provided
                if len(obs_data) != 0:
                    MetaModel.SeqBME[strKey] = SeqBME
                    MetaModel.SeqKLD[strKey] = SeqKLD
                if len(MetaModel.valid_likelihoods) != 0:
                    MetaModel.SeqDistHellinger[strKey] = SeqDistHellinger
                if mc_ref and pce:
                    MetaModel.seqRMSEMean[strKey] = seqRMSEMean
                    MetaModel.seqRMSEStd[strKey] = seqRMSEStd

        return MetaModel

    # -------------------------------------------------------------------------
    def util_VarBasedDesign(self, X_can, index, util_func='Entropy'):
        """
        Computes the exploitation scores based on:
        active learning MacKay(ALM) and active learning Cohn (ALC)
        Paper: Sequential Design with Mutual Information for Computer
        Experiments (MICE): Emulation of a Tsunami Model by Beck and Guillas
        (2016)

        Parameters
        ----------
        X_can : array of shape (n_samples, n_params)
            Candidate samples.
        index : int
            Model output index.
        UtilMethod : string, optional
            Exploitation utility function. The default is 'Entropy'.

        Returns
        -------
        float
            Score.

        """
        MetaModel = self.MetaModel
        ED_X = MetaModel.ExpDesign.X
        out_dict_y = MetaModel.ExpDesign.Y
        out_names = MetaModel.ModelObj.Output.names

        # Run the Metamodel for the candidate
        X_can = X_can.reshape(1, -1)
        Y_PC_can, std_PC_can = MetaModel.eval_metamodel(samples=X_can)

        if util_func.lower() == 'alm':
            # ----- Entropy/MMSE/active learning MacKay(ALM)  -----
            # Compute perdiction variance of the old model
            canPredVar = {key: std_PC_can[key]**2 for key in out_names}

            varPCE = np.zeros((len(out_names), X_can.shape[0]))
            for KeyIdx, key in enumerate(out_names):
                varPCE[KeyIdx] = np.max(canPredVar[key], axis=1)
            score = np.max(varPCE, axis=0)

        elif util_func.lower() == 'eigf':
            # ----- Expected Improvement for Global fit -----
            # Find closest EDX to the candidate
            distances = distance.cdist(ED_X, X_can, 'euclidean')
            index = np.argmin(distances)

            # Compute perdiction error and variance of the old model
            predError = {key: Y_PC_can[key] for key in out_names}
            canPredVar = {key: std_PC_can[key]**2 for key in out_names}

            # Compute perdiction error and variance of the old model
            # Eq (5) from Liu et al.(2018)
            EIGF_PCE = np.zeros((len(out_names), X_can.shape[0]))
            for KeyIdx, key in enumerate(out_names):
                residual = predError[key] - out_dict_y[key][int(index)]
                var = canPredVar[key]
                EIGF_PCE[KeyIdx] = np.max(residual**2 + var, axis=1)
            score = np.max(EIGF_PCE, axis=0)

        return -1 * score   # -1 is for minimization instead of maximization

    # -------------------------------------------------------------------------
    def util_BayesianActiveDesign(self, X_can, sigma2Dict, var='DKL'):
        """
        Computes scores based on Bayesian active design criterion (var).

        It is based on the following paper:
        Oladyshkin, Sergey, Farid Mohammadi, Ilja Kroeker, and Wolfgang Nowak.
        "Bayesian3 active learning for the gaussian process emulator using
        information theory." Entropy 22, no. 8 (2020): 890.

        Parameters
        ----------
        X_can : array of shape (n_samples, n_params)
            Candidate samples.
        sigma2Dict : dict
            A dictionary containing the measurement errors (sigma^2).
        var : string, optional
            BAL design criterion. The default is 'DKL'.

        Returns
        -------
        float
            Score.

        """

        # Evaluate the PCE metamodels at that location ???
        Y_mean_can, Y_std_can = self.MetaModel.eval_metamodel(
            samples=np.array([X_can])
            )

        # Get the data
        obs_data = self.observations
        n_obs = self.Model.n_obs
        # TODO: Analytical DKL
        # Sample a distribution for a normal dist
        # with Y_mean_can as the mean and Y_std_can as std.

        # priorMean, priorSigma2, Obs = np.empty((0)),np.empty((0)),np.empty((0))

        # for key in list(Y_mean_can):
        #     # concatenate the measurement error
        #     Obs = np.hstack((Obs,ObservationData[key]))

        #     # concatenate the mean and variance of prior predictive
        #     means, stds = Y_mean_can[key][0], Y_std_can[key][0]
        #     priorMean = np.hstack((priorSigma2,means))
        #     priorSigma2 = np.hstack((priorSigma2,stds**2))

        # # Covariance Matrix of prior
        # covPrior = np.zeros((priorSigma2.shape[0], priorSigma2.shape[0]), float)
        # np.fill_diagonal(covPrior, priorSigma2)

        # # Covariance Matrix of Likelihood
        # covLikelihood = np.zeros((sigma2Dict.shape[0], sigma2Dict.shape[0]), float)
        # np.fill_diagonal(covLikelihood, sigma2Dict)

        # # Calculate moments of the posterior (Analytical derivation)
        # n = priorSigma2.shape[0]
        # covPost = np.dot(np.dot(covPrior,np.linalg.inv(covPrior+(covLikelihood/n))),covLikelihood/n)

        # meanPost = np.dot(np.dot(covPrior,np.linalg.inv(covPrior+(covLikelihood/n))) , Obs) + \
        #             np.dot(np.dot(covPrior,np.linalg.inv(covPrior+(covLikelihood/n))),
        #                     priorMean/n)
        # # Compute DKL from prior to posterior
        # term1 = np.trace(np.dot(np.linalg.inv(covPrior),covPost))
        # deltaMean = priorMean-meanPost
        # term2 = np.dot(np.dot(deltaMean,np.linalg.inv(covPrior)),deltaMean[:,None])
        # term3 = np.log(np.linalg.det(covPrior)/np.linalg.det(covPost))
        # DKL = 0.5 * (term1 + term2 - n + term3)[0]

        # ---------- Inner MC simulation for computing Utility Value ----------
        # Estimation of the integral via Monte Varlo integration
        MCsize = 20000
        ESS = 0

        while ((ESS > MCsize) or (ESS < 1)):

            # Sample a distribution for a normal dist
            # with Y_mean_can as the mean and Y_std_can as std.
            Y_MC, std_MC = {}, {}
            logPriorLikelihoods = np.zeros((MCsize))
            for key in list(Y_mean_can):
                means, stds = Y_mean_can[key][0], Y_std_can[key][0]
                # cov = np.zeros((means.shape[0], means.shape[0]), float)
                # np.fill_diagonal(cov, stds**2)

                Y_MC[key] = np.zeros((MCsize, n_obs))
                logsamples = np.zeros((MCsize, n_obs))
                for i in range(n_obs):
                    NormalDensity = stats.norm(means[i], stds[i])
                    Y_MC[key][:, i] = NormalDensity.rvs(MCsize)
                    logsamples[:, i] = NormalDensity.logpdf(Y_MC[key][:, i])

                logPriorLikelihoods = np.sum(logsamples, axis=1)
                std_MC[key] = np.zeros((MCsize, means.shape[0]))

            #  Likelihood computation (Comparison of data and simulation
            #  results via PCE with candidate design)
            likelihoods = self.__normpdf(Y_MC, std_MC, obs_data, sigma2Dict)

            # Check the Effective Sample Size (1<ESS<MCsize)
            ESS = 1 / np.sum(np.square(likelihoods/np.nansum(likelihoods)))

            # Enlarge sample size if it doesn't fulfill the criteria
            if ((ESS > MCsize) or (ESS < 1)):
                MCsize *= 10
                ESS = 0

        # Rejection Step
        # Random numbers between 0 and 1
        unif = np.random.rand(1, MCsize)[0]

        # Reject the poorly performed prior
        accepted = (likelihoods/np.max(likelihoods)) >= unif

        # Prior-based estimation of BME
        logBME = np.log(np.nanmean(likelihoods))

        # Posterior-based expectation of likelihoods
        postLikelihoods = likelihoods[accepted]
        postExpLikelihoods = np.mean(np.log(postLikelihoods))

        # Posterior-based expectation of prior densities
        postExpPrior = np.mean(logPriorLikelihoods[accepted])

        # Utility function Eq.2 in Ref. (2)
        # Posterior covariance matrix after observing data y
        # Kullback-Leibler Divergence (Sergey's paper)
        if var == 'DKL':

            # TODO: Calculate the correction factor for BME
            # BMECorrFactor = self.BME_Corr_Weight(PCE_SparseBayes_can,
            #                                      ObservationData, sigma2Dict)
            # BME += BMECorrFactor
            # Haun et al implementation
            # U_J_d = np.mean(np.log(Likelihoods[Likelihoods!=0])- logBME)
            U_J_d = postExpLikelihoods - logBME

        # Marginal log likelihood
        elif var == 'BME':
            U_J_d = logBME

        # Entropy-based information gain
        elif var == 'infEntropy':
            logBME = np.log(np.nanmean(likelihoods))
            infEntropy = logBME - postExpPrior - postExpLikelihoods
            U_J_d = infEntropy * -1  # -1 for minimization

        # Bayesian information criterion
        elif var == 'BIC':
            coeffs = self.MetaModel.coeffs_dict.values()
            nModelParams = max(len(v) for val in coeffs for v in val.values())
            maxL = np.nanmax(likelihoods)
            U_J_d = -2 * np.log(maxL) + np.log(n_obs) * nModelParams

        # Akaike information criterion
        elif var == 'AIC':
            coeffs = self.MetaModel.coeffs_dict.values()
            nModelParams = max(len(v) for val in coeffs for v in val.values())
            maxlogL = np.log(np.nanmax(likelihoods))
            AIC = -2 * maxlogL + 2 * nModelParams
            # 2 * nModelParams * (nModelParams+1) / (n_obs-nModelParams-1)
            penTerm = 0
            U_J_d = 1*(AIC + penTerm)

        # Deviance information criterion
        elif var == 'DIC':
            # D_theta_bar = np.mean(-2 * Likelihoods)
            N_star_p = 0.5 * np.var(np.log(likelihoods[likelihoods != 0]))
            Likelihoods_theta_mean = self.__normpdf(
                Y_mean_can, Y_std_can, obs_data, sigma2Dict
                )
            DIC = -2 * np.log(Likelihoods_theta_mean) + 2 * N_star_p

            U_J_d = DIC

        else:
            print('The algorithm you requested has not been implemented yet!')

        # Handle inf and NaN (replace by zero)
        if np.isnan(U_J_d) or U_J_d == -np.inf or U_J_d == np.inf:
            U_J_d = 0.0

        # Clear memory
        del likelihoods
        del Y_MC
        del std_MC
        gc.collect(generation=2)

        return -1 * U_J_d   # -1 is for minimization instead of maximization

    # -------------------------------------------------------------------------
    def update_metamodel(self, MetaModel, output, y_hat_can, univ_p_val, index,
                         new_pca=False):
        BasisIndices = MetaModel.basis_dict[output]["y_"+str(index+1)]
        clf_poly = MetaModel.clf_poly[output]["y_"+str(index+1)]
        Mn = clf_poly.coef_
        Sn = clf_poly.sigma_
        beta = clf_poly.alpha_
        active = clf_poly.active_
        Psi = self.MetaModel.create_psi(BasisIndices, univ_p_val)

        Sn_new_inv = np.linalg.inv(Sn)
        Sn_new_inv += beta * np.dot(Psi[:, active].T, Psi[:, active])
        Sn_new = np.linalg.inv(Sn_new_inv)

        Mn_new = np.dot(Sn_new_inv, Mn[active]).reshape(-1, 1)
        Mn_new += beta * np.dot(Psi[:, active].T, y_hat_can)
        Mn_new = np.dot(Sn_new, Mn_new).flatten()

        # Compute the old and new moments of PCEs
        mean_old = Mn[0]
        mean_new = Mn_new[0]
        std_old = np.sqrt(np.sum(np.square(Mn[1:])))
        std_new = np.sqrt(np.sum(np.square(Mn_new[1:])))

        # Back transformation if PCA is selected.
        if MetaModel.dim_red_method.lower() == 'pca':
            old_pca = MetaModel.pca[output]
            mean_old = old_pca.mean_[index]
            mean_old += np.sum(mean_old * old_pca.components_[:, index])
            std_old = np.sqrt(np.sum(std_old**2 *
                                     old_pca.components_[:, index]**2))
            mean_new = new_pca.mean_[index]
            mean_new += np.sum(mean_new * new_pca.components_[:, index])
            std_new = np.sqrt(np.sum(std_new**2 *
                                     new_pca.components_[:, index]**2))
            # print(f"mean_old: {mean_old:.2f} mean_new: {mean_new:.2f}")
            # print(f"std_old: {std_old:.2f} std_new: {std_new:.2f}")
        # Store the old and new moments of PCEs
        results = {
            'mean_old': mean_old,
            'mean_new': mean_new,
            'std_old': std_old,
            'std_new': std_new
            }
        return results

    # -------------------------------------------------------------------------
    def util_BayesianDesign_old(self, X_can, X_MC, sigma2Dict, var='DKL'):
        """
        Computes scores based on Bayesian sequential design criterion (var).

        Parameters
        ----------
        X_can : array of shape (n_samples, n_params)
            Candidate samples.
        sigma2Dict : dict
            A dictionary containing the measurement errors (sigma^2).
        var : string, optional
            Bayesian design criterion. The default is 'DKL'.

        Returns
        -------
        float
            Score.

        """

        # To avoid changes ub original aPCE object
        Model = self.Model
        MetaModel = deepcopy(self.MetaModel)
        old_EDY = MetaModel.ExpDesign.Y

        # Evaluate the PCE metamodels using the candidate design
        Y_PC_can, Y_std_can = self.MetaModel.eval_metamodel(
            samples=np.array([X_can])
            )

        # Generate y from posterior predictive
        m_size = 100
        y_hat_samples = {}
        for idx, key in enumerate(Model.Output.names):
            means, stds = Y_PC_can[key][0], Y_std_can[key][0]
            y_hat_samples[key] = np.random.multivariate_normal(
                means, np.diag(stds), m_size)

        # Create the SparseBayes-based PCE metamodel:
        MetaModel.input_obj.poly_coeffs_flag = False
        univ_p_val = self.MetaModel.univ_basis_vals(X_can)
        G_n_m_all = np.zeros((m_size, len(Model.Output.names), Model.n_obs))

        for i in range(m_size):
            for idx, key in enumerate(Model.Output.names):
                if MetaModel.dim_red_method.lower() == 'pca':
                    # Equal number of components
                    new_outputs = np.vstack(
                        (old_EDY[key], y_hat_samples[key][i])
                        )
                    new_pca, _ = MetaModel.pca_transformation(new_outputs)
                    target = new_pca.transform(
                        y_hat_samples[key][i].reshape(1, -1)
                        )[0]
                else:
                    new_pca, target = False, y_hat_samples[key][i]

                for j in range(len(target)):

                    # Update surrogate
                    result = self.update_metamodel(
                        MetaModel, key, target[j], univ_p_val, j, new_pca)

                    # Compute Expected Information Gain (Eq. 39)
                    G_n_m = np.log(result['std_old']/result['std_new']) - 1./2
                    G_n_m += result['std_new']**2 / (2*result['std_old']**2)
                    G_n_m += (result['mean_new'] - result['mean_old'])**2 /\
                        (2*result['std_old']**2)

                    G_n_m_all[i, idx, j] = G_n_m

        U_J_d = G_n_m_all.mean(axis=(1, 2)).mean()
        return -1 * U_J_d

    # -------------------------------------------------------------------------
    def util_BayesianDesign(self, X_can, X_MC, sigma2Dict, var='DKL'):
        """
        Computes scores based on Bayesian sequential design criterion (var).

        Parameters
        ----------
        X_can : array of shape (n_samples, n_params)
            Candidate samples.
        sigma2Dict : dict
            A dictionary containing the measurement errors (sigma^2).
        var : string, optional
            Bayesian design criterion. The default is 'DKL'.

        Returns
        -------
        float
            Score.

        """

        # To avoid changes ub original aPCE object
        Model = self.Model
        MetaModel = deepcopy(self.MetaModel)
        out_names = MetaModel.ModelObj.Output.names
        if X_can.ndim == 1:
            X_can = X_can.reshape(1, -1)

        # Compute the mean and std based on the MetaModel
        # pce_means, pce_stds = self._compute_pce_moments(MetaModel)
        if var == 'ALC':
            Y_MC, Y_MC_std = MetaModel.eval_metamodel(samples=X_MC)

        # Old Experimental design
        oldExpDesignX = MetaModel.ExpDesign.X
        oldExpDesignY = MetaModel.ExpDesign.Y

        # Evaluate the PCE metamodels at that location ???
        Y_PC_can, Y_std_can = MetaModel.eval_metamodel(samples=X_can)

        # Add all suggestion as new ExpDesign
        NewExpDesignX = np.vstack((oldExpDesignX, X_can))

        NewExpDesignY = {}
        for key in oldExpDesignY.keys():
            try:
                NewExpDesignY[key] = np.vstack((oldExpDesignY[key],
                                                Y_PC_can[key]))
            except:
                NewExpDesignY[key] = oldExpDesignY[key]

        MetaModel.ExpDesign.sampling_method = 'user'
        MetaModel.ExpDesign.X = NewExpDesignX
        MetaModel.ExpDesign.Y = NewExpDesignY

        # Train the model for the observed data using x_can
        MetaModel.input_obj.poly_coeffs_flag = False
        MetaModel.train_norm_design(parallel=False)
        PCE_Model_can = MetaModel

        if var.lower() == 'mi':
            # Mutual information based on Krause et al
            # Adapted from Beck & Guillas (MICE) paper
            _, std_PC_can = PCE_Model_can.eval_metamodel(samples=X_can)
            std_can = {key: std_PC_can[key] for key in out_names}

            std_old = {key: Y_std_can[key] for key in out_names}

            varPCE = np.zeros((len(out_names)))
            for i, key in enumerate(out_names):
                varPCE[i] = np.mean(std_old[key]**2/std_can[key]**2)
            score = np.mean(varPCE)

            return -1 * score

        elif var.lower() == 'alc':
            # Active learning based on Gramyc and Lee
            # Adaptive design and analysis of supercomputer experiments Techno-
            # metrics, 51 (2009), pp. 130–145.

            # Evaluate the MetaModel at the given samples
            Y_MC_can, Y_MC_std_can = PCE_Model_can.eval_metamodel(samples=X_MC)

            # Compute the score
            score = []
            for i, key in enumerate(out_names):
                pce_var = Y_MC_std_can[key]**2
                pce_var_can = Y_MC_std[key]**2
                score.append(np.mean(pce_var-pce_var_can, axis=0))
            score = np.mean(score)

            return -1 * score

        # ---------- Inner MC simulation for computing Utility Value ----------
        # Estimation of the integral via Monte Varlo integration
        MCsize = X_MC.shape[0]
        ESS = 0

        while ((ESS > MCsize) or (ESS < 1)):

            # Enriching Monte Carlo samples if need be
            if ESS != 0:
                X_MC = self.MetaModel.ExpDesign.generate_samples(
                    MCsize, 'random'
                    )

            # Evaluate the MetaModel at the given samples
            Y_MC, std_MC = PCE_Model_can.eval_metamodel(samples=X_MC)

            # Likelihood computation (Comparison of data and simulation
            # results via PCE with candidate design)
            likelihoods = self.__normpdf(
                Y_MC, std_MC, self.observations, sigma2Dict
                )

            # Check the Effective Sample Size (1<ESS<MCsize)
            ESS = 1 / np.sum(np.square(likelihoods/np.sum(likelihoods)))

            # Enlarge sample size if it doesn't fulfill the criteria
            if ((ESS > MCsize) or (ESS < 1)):
                print("--- increasing MC size---")
                MCsize *= 10
                ESS = 0

        # Rejection Step
        # Random numbers between 0 and 1
        unif = np.random.rand(1, MCsize)[0]

        # Reject the poorly performed prior
        accepted = (likelihoods/np.max(likelihoods)) >= unif

        # -------------------- Utility functions --------------------
        # Utility function Eq.2 in Ref. (2)
        # Kullback-Leibler Divergence (Sergey's paper)
        if var == 'DKL':

            # Prior-based estimation of BME
            logBME = np.log(np.nanmean(likelihoods, dtype=np.float128))

            # Posterior-based expectation of likelihoods
            postLikelihoods = likelihoods[accepted]
            postExpLikelihoods = np.mean(np.log(postLikelihoods))

            # Haun et al implementation
            U_J_d = np.mean(np.log(likelihoods[likelihoods != 0]) - logBME)

            # U_J_d = np.sum(G_n_m_all)
            # Ryan et al (2014) implementation
            # importanceWeights = Likelihoods[Likelihoods!=0]/np.sum(Likelihoods[Likelihoods!=0])
            # U_J_d = np.mean(importanceWeights*np.log(Likelihoods[Likelihoods!=0])) - logBME

            # U_J_d = postExpLikelihoods - logBME

        # Marginal likelihood
        elif var == 'BME':

            # Prior-based estimation of BME
            logBME = np.log(np.nanmean(likelihoods))
            U_J_d = logBME

        # Bayes risk likelihood
        elif var == 'BayesRisk':

            U_J_d = -1 * np.var(likelihoods)

        # Entropy-based information gain
        elif var == 'infEntropy':
            # Prior-based estimation of BME
            logBME = np.log(np.nanmean(likelihoods))

            # Posterior-based expectation of likelihoods
            postLikelihoods = likelihoods[accepted] / np.nansum(likelihoods[accepted])
            postExpLikelihoods = np.mean(np.log(postLikelihoods))

            # Posterior-based expectation of prior densities
            postExpPrior = np.mean(logPriorLikelihoods[accepted])

            infEntropy = logBME - postExpPrior - postExpLikelihoods

            U_J_d = infEntropy * -1  # -1 for minimization

        # D-Posterior-precision
        elif var == 'DPP':
            X_Posterior = X_MC[accepted]
            # covariance of the posterior parameters
            U_J_d = -np.log(np.linalg.det(np.cov(X_Posterior)))

        # A-Posterior-precision
        elif var == 'APP':
            X_Posterior = X_MC[accepted]
            # trace of the posterior parameters
            U_J_d = -np.log(np.trace(np.cov(X_Posterior)))

        else:
            print('The algorithm you requested has not been implemented yet!')

        # Clear memory
        del likelihoods
        del Y_MC
        del std_MC
        gc.collect(generation=2)

        return -1 * U_J_d   # -1 is for minimization instead of maximization

    # -------------------------------------------------------------------------
    def subdomain(self, Bounds, n_new_samples):
        """
        Divides a domain defined by Bounds into sub domains.

        Parameters
        ----------
        Bounds : list of tuples
            List of lower and upper bounds.
        n_new_samples : TYPE
            DESCRIPTION.

        Returns
        -------
        Subdomains : TYPE
            DESCRIPTION.

        """
        n_params = self.MetaModel.n_params
        n_subdomains = n_new_samples + 1
        LinSpace = np.zeros((n_params, n_subdomains))

        for i in range(n_params):
            LinSpace[i] = np.linspace(start=Bounds[i][0], stop=Bounds[i][1],
                                      num=n_subdomains)
        Subdomains = []
        for k in range(n_subdomains-1):
            mylist = []
            for i in range(n_params):
                mylist.append((LinSpace[i, k+0], LinSpace[i, k+1]))
            Subdomains.append(tuple(mylist))

        return Subdomains

    # -------------------------------------------------------------------------
    def run_util_func(self, method, candidates, index, sigma2Dict=None,
                      var=None, X_MC=None):
        """
        Runs the utility function based on the given method.

        Parameters
        ----------
        method : string
            Exploitation method: `VarOptDesign`, `BayesActDesign` and
            `BayesOptDesign`.
        candidates : array of shape (n_samples, n_params)
            All candidate parameter sets.
        index : int
            ExpDesign index.
        sigma2Dict : dict, optional
            A dictionary containing the measurement errors (sigma^2). The
            default is None.
        var : string, optional
            Utility function. The default is None.
        X_MC : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        index : TYPE
            DESCRIPTION.
        List
            Scores.

        """

        if method.lower() == 'varoptdesign':
            # U_J_d = self.util_VarBasedDesign(candidates, index, var)
            U_J_d = np.zeros((candidates.shape[0]))
            for idx, X_can in tqdm(enumerate(candidates), ascii=True,
                                   desc="varoptdesign"):
                U_J_d[idx] = self.util_VarBasedDesign(X_can, index, var)

        elif method.lower() == 'bayesactdesign':
            NCandidate = candidates.shape[0]
            U_J_d = np.zeros((NCandidate))
            for idx, X_can in tqdm(enumerate(candidates), ascii=True,
                                   desc="OptBayesianDesign"):
                U_J_d[idx] = self.util_BayesianActiveDesign(X_can, sigma2Dict,
                                                            var)
        elif method.lower() == 'bayesoptdesign':
            NCandidate = candidates.shape[0]
            U_J_d = np.zeros((NCandidate))
            for idx, X_can in tqdm(enumerate(candidates), ascii=True,
                                   desc="OptBayesianDesign"):
                U_J_d[idx] = self.util_BayesianDesign(X_can, X_MC, sigma2Dict,
                                                      var)
        return (index, -1 * U_J_d)

    # -------------------------------------------------------------------------
    def dual_annealing(self, method, Bounds, sigma2Dict, var, Run_No,
                       verbose=False):
        """
        Exploration algorithim to find the optimum parameter space.

        Parameters
        ----------
        method : string
            Exploitation method: `VarOptDesign`, `BayesActDesign` and
            `BayesOptDesign`.
        Bounds : list of tuples
            List of lower and upper boundaries of parameters.
        sigma2Dict : dict
            A dictionary containing the measurement errors (sigma^2).
        Run_No : int
            Run number.
        verbose : bool, optional
            Print out a summary. The default is False.

        Returns
        -------
        Run_No : int
            Run number.
        array
            Optimial candidate.

        """

        Model = self.Model
        max_func_itr = self.MetaModel.ExpDesign.max_func_itr

        if method == 'VarOptDesign':
            Res_Global = opt.dual_annealing(self.util_VarBasedDesign,
                                            bounds=Bounds,
                                            args=(Model, var),
                                            maxfun=max_func_itr)

        elif method == 'BayesOptDesign':
            Res_Global = opt.dual_annealing(self.util_BayesianDesign,
                                            bounds=Bounds,
                                            args=(Model, sigma2Dict, var),
                                            maxfun=max_func_itr)

        if verbose:
            print(f"global minimum: xmin = {Res_Global.x}, "
                  f"f(xmin) = {Res_Global.fun:.6f}, nfev = {Res_Global.nfev}")

        return (Run_No, Res_Global.x)

    # -------------------------------------------------------------------------
    def tradoff_weights(self, tradeoff_scheme, old_EDX, old_EDY):
        """
        Calculates weights for exploration scores based on the requested
        scheme: `None`, `equal`, `epsilon-decreasing` and `adaptive`.

        `None`: No exploration.
        `equal`: Same weights for exploration and exploitation scores.
        `epsilon-decreasing`: Start with more exploration and increase the
            influence of exploitation along the way with a exponential decay
            function
        `adaptive`: An adaptive method based on:
            Liu, Haitao, Jianfei Cai, and Yew-Soon Ong. "An adaptive sampling
            approach for Kriging metamodeling by maximizing expected prediction
            error." Computers & Chemical Engineering 106 (2017): 171-182.

        Parameters
        ----------
        tradeoff_scheme : string
            Trade-off scheme for exloration and exploitation scores.
        old_EDX : array (n_samples, n_params)
            Old experimental design (training points).
        old_EDY : dict
            Old model responses (targets).

        Returns
        -------
        exploration_weight : float
            Exploration weight.
        exploitation_weight: float
            Exploitation weight.

        """
        if tradeoff_scheme is None:
            exploration_weight = 0

        elif tradeoff_scheme == 'equal':
            exploration_weight = 0.5

        elif tradeoff_scheme == 'epsilon-decreasing':
            # epsilon-decreasing scheme
            # Start with more exploration and increase the influence of
            # exploitation along the way with a exponential decay function
            initNSamples = self.MetaModel.ExpDesign.n_init_samples
            n_max_samples = self.MetaModel.ExpDesign.n_max_samples

            itrNumber = (self.MetaModel.ExpDesign.X.shape[0] - initNSamples)
            itrNumber //= self.MetaModel.ExpDesign.n_new_samples

            tau2 = -(n_max_samples-initNSamples-1) / np.log(1e-8)
            exploration_weight = signal.exponential(n_max_samples-initNSamples,
                                                    0, tau2, False)[itrNumber]

        elif tradeoff_scheme == 'adaptive':

            # Extract itrNumber
            initNSamples = self.MetaModel.ExpDesign.n_init_samples
            n_max_samples = self.MetaModel.ExpDesign.n_max_samples
            itrNumber = (self.MetaModel.ExpDesign.X.shape[0] - initNSamples)
            itrNumber //= self.MetaModel.ExpDesign.n_new_samples

            if itrNumber == 0:
                exploration_weight = 0.5
            else:
                # New adaptive trade-off according to Liu et al. (2017)
                # Mean squared error for last design point
                last_EDX = old_EDX[-1].reshape(1, -1)
                lastPCEY, _ = self.MetaModel.eval_metamodel(samples=last_EDX)
                pce_y = np.array(list(lastPCEY.values()))[:, 0]
                y = np.array(list(old_EDY.values()))[:, -1, :]
                mseError = mean_squared_error(pce_y, y)

                # Mean squared CV - error for last design point
                pce_y_prev = np.array(list(self._y_hat_prev.values()))[:, 0]
                mseCVError = mean_squared_error(pce_y_prev, y)

                exploration_weight = min([0.5*mseError/mseCVError, 1])

        # Exploitation weight
        exploitation_weight = 1 - exploration_weight

        return exploration_weight, exploitation_weight

    # -------------------------------------------------------------------------
    def opt_SeqDesign(self, sigma2, n_candidates=5, var='DKL'):
        """
        Runs optimal sequential design.

        Parameters
        ----------
        sigma2 : dict, optional
            A dictionary containing the measurement errors (sigma^2). The
            default is None.
        n_candidates : int, optional
            Number of candidate samples. The default is 5.
        var : string, optional
            Utility function. The default is None.

        Raises
        ------
        NameError
            Wrong utility function.

        Returns
        -------
        Xnew : array (n_samples, n_params)
            Selected new training point(s).
        """

        # Initialization
        MetaModel = self.MetaModel
        Bounds = MetaModel.bound_tuples
        n_new_samples = MetaModel.ExpDesign.n_new_samples
        explore_method = MetaModel.ExpDesign.explore_method
        exploit_method = MetaModel.ExpDesign.exploit_method
        n_cand_groups = MetaModel.ExpDesign.n_cand_groups
        tradeoff_scheme = MetaModel.ExpDesign.tradeoff_scheme

        old_EDX = MetaModel.ExpDesign.X
        old_EDY = MetaModel.ExpDesign.Y.copy()
        ndim = MetaModel.ExpDesign.X.shape[1]
        OutputNames = MetaModel.ModelObj.Output.names

        # -----------------------------------------
        # ----------- CUSTOMIZED METHODS ----------
        # -----------------------------------------
        # Utility function exploit_method provided by user
        if exploit_method.lower() == 'user':

            Xnew, filteredSamples = MetaModel.ExpDesign.ExploitFunction(self)

            print("\n")
            print("\nXnew:\n", Xnew)

            return Xnew, filteredSamples

        # -----------------------------------------
        # ---------- EXPLORATION METHODS ----------
        # -----------------------------------------
        if explore_method == 'dual annealing':
            # ------- EXPLORATION: OPTIMIZATION -------
            import time
            start_time = time.time()

            # Divide the domain to subdomains
            args = []
            subdomains = self.subdomain(Bounds, n_new_samples)
            for i in range(n_new_samples):
                args.append((exploit_method, subdomains[i], sigma2, var, i))

            # Multiprocessing
            pool = multiprocessing.Pool(multiprocessing.cpu_count())

            # With Pool.starmap_async()
            results = pool.starmap_async(self.dual_annealing, args).get()

            # Close the pool
            pool.close()

            Xnew = np.array([results[i][1] for i in range(n_new_samples)])

            print("\nXnew:\n", Xnew)

            elapsed_time = time.time() - start_time
            print("\n")
            print(f"elapsed_time: {round(elapsed_time,2)} sec.")
            print('-'*20)

        elif explore_method == 'LOOCV':
            # -----------------------------------------------------------------
            # TODO: LOOCV model construnction based on Feng et al. (2020)
            # 'LOOCV':
            # Initilize the ExploitScore array

            # Generate random samples
            allCandidates = MetaModel.ExpDesign.generate_samples(n_candidates,
                                                                'random')

            # Construct error model based on LCerror
            errorModel = MetaModel.create_ModelError(old_EDX, self.LCerror)
            self.errorModel.append(copy(errorModel))

            # Evaluate the error models for allCandidates
            eLCAllCands, _ = errorModel.eval_errormodel(allCandidates)
            # Select the maximum as the representative error
            eLCAllCands = np.dstack(eLCAllCands.values())
            eLCAllCandidates = np.max(eLCAllCands, axis=1)[:, 0]

            # Normalize the error w.r.t the maximum error
            scoreExploration = eLCAllCandidates / np.sum(eLCAllCandidates)

        else:
            # ------- EXPLORATION: SPACE-FILLING DESIGN -------
            # Generate candidate samples from Exploration class
            explore = Exploration(MetaModel, n_candidates)
            explore.w = 100  # * ndim #500
            # Select criterion (mc-intersite-proj-th, mc-intersite-proj)
            explore.mc_criterion = 'mc-intersite-proj'
            allCandidates, scoreExploration = explore.get_exploration_samples()

            # Temp: ---- Plot all candidates -----
            if ndim == 2:
                def plotter(points, allCandidates, Method,
                            scoreExploration=None):
                    if Method == 'Voronoi':
                        from scipy.spatial import Voronoi, voronoi_plot_2d
                        vor = Voronoi(points)
                        fig = voronoi_plot_2d(vor)
                        ax1 = fig.axes[0]
                    else:
                        fig = plt.figure()
                        ax1 = fig.add_subplot(111)
                    ax1.scatter(points[:, 0], points[:, 1], s=10, c='r',
                                marker="s", label='Old Design Points')
                    ax1.scatter(allCandidates[:, 0], allCandidates[:, 1], s=10,
                                c='b', marker="o", label='Design candidates')
                    for i in range(points.shape[0]):
                        txt = 'p'+str(i+1)
                        ax1.annotate(txt, (points[i, 0], points[i, 1]))
                    if scoreExploration is not None:
                        for i in range(allCandidates.shape[0]):
                            txt = str(round(scoreExploration[i], 5))
                            ax1.annotate(txt, (allCandidates[i, 0],
                                               allCandidates[i, 1]))

                    plt.xlim(self.bound_tuples[0])
                    plt.ylim(self.bound_tuples[1])
                    # plt.show()
                    plt.legend(loc='upper left')

        # -----------------------------------------
        # --------- EXPLOITATION METHODS ----------
        # -----------------------------------------
        if exploit_method == 'BayesOptDesign' or\
           exploit_method == 'BayesActDesign':

            # ------- Calculate Exoploration weight -------
            # Compute exploration weight based on trade off scheme
            explore_w, exploit_w = self.tradoff_weights(tradeoff_scheme,
                                                        old_EDX,
                                                        old_EDY)
            print(f"\n Exploration weight={explore_w:0.3f} "
                  f"Exploitation weight={exploit_w:0.3f}\n")

            # ------- EXPLOITATION: BayesOptDesign & ActiveLearning -------
            if explore_w != 1.0:

                # Create a sample pool for rejection sampling
                MCsize = 15000
                X_MC = MetaModel.ExpDesign.generate_samples(MCsize, 'random')
                candidates = MetaModel.ExpDesign.generate_samples(
                    MetaModel.ExpDesign.max_func_itr, 'latin_hypercube')

                # Split the candidates in groups for multiprocessing
                split_cand = np.array_split(
                    candidates, n_cand_groups, axis=0
                    )

                results = Parallel(n_jobs=-1, backend='threading')(
                        delayed(self.run_util_func)(
                            exploit_method, split_cand[i], i, sigma2, var, X_MC)
                        for i in range(n_cand_groups))
                # out = map(self.run_util_func,
                #           [exploit_method]*n_cand_groups,
                #           split_cand,
                #           range(n_cand_groups),
                #           [sigma2] * n_cand_groups,
                #           [var] * n_cand_groups,
                #           [X_MC] * n_cand_groups
                #           )
                # results = list(out)

                # Retrieve the results and append them
                U_J_d = np.concatenate([results[NofE][1] for NofE in
                                        range(n_cand_groups)])

                # Check if all scores are inf
                if np.isinf(U_J_d).all() or np.isnan(U_J_d).all():
                    U_J_d = np.ones(len(U_J_d))

                # Get the expected value (mean) of the Utility score
                # for each cell
                if explore_method == 'Voronoi':
                    U_J_d = np.mean(U_J_d.reshape(-1, n_candidates), axis=1)

                # create surrogate model for U_J_d
                from sklearn.preprocessing import MinMaxScaler
                # Take care of inf entries
                good_indices = [i for i, arr in enumerate(U_J_d)
                                if np.isfinite(arr).all()]
                scaler = MinMaxScaler()
                X_S = scaler.fit_transform(candidates[good_indices])
                gp = MetaModel.gaussian_process_emulator(
                    X_S, U_J_d[good_indices], autoSelect=True
                    )
                U_J_d = gp.predict(scaler.transform(allCandidates))

                # Normalize U_J_d
                norm_U_J_d = U_J_d / np.sum(U_J_d)
                print("norm_U_J_d:\n", norm_U_J_d)
            else:
                norm_U_J_d = np.zeros((len(scoreExploration)))

            # ------- Calculate Total score -------
            # ------- Trade off between EXPLORATION & EXPLOITATION -------
            # Total score
            totalScore = exploit_w * norm_U_J_d
            totalScore += explore_w * scoreExploration

            # temp: Plot
            # dim = self.ExpDesign.X.shape[1]
            # if dim == 2:
            #     plotter(self.ExpDesign.X, allCandidates, explore_method)

            # ------- Select the best candidate -------
            # find an optimal point subset to add to the initial design by
            # maximization of the utility score and taking care of NaN values
            temp = totalScore.copy()
            temp[np.isnan(totalScore)] = -np.inf
            sorted_idxtotalScore = np.argsort(temp)[::-1]
            bestIdx = sorted_idxtotalScore[:n_new_samples]

            # select the requested number of samples
            if explore_method == 'Voronoi':
                Xnew = np.zeros((n_new_samples, ndim))
                for i, idx in enumerate(bestIdx):
                    X_can = explore.closestPoints[idx]

                    # Calculate the maxmin score for the region of interest
                    newSamples, maxminScore = explore.get_mc_samples(X_can)

                    # select the requested number of samples
                    Xnew[i] = newSamples[np.argmax(maxminScore)]
            else:
                Xnew = allCandidates[sorted_idxtotalScore[:n_new_samples]]

        elif exploit_method == 'VarOptDesign':
            # ------- EXPLOITATION: VarOptDesign -------
            UtilMethod = var

            # ------- Calculate Exoploration weight -------
            # Compute exploration weight based on trade off scheme
            explore_w, exploit_w = self.tradoff_weights(tradeoff_scheme,
                                                        old_EDX,
                                                        old_EDY)
            print(f"\nweightExploration={explore_w:0.3f} "
                  f"weightExploitation={exploit_w:0.3f}")

            # Generate candidate samples from Exploration class
            nMeasurement = old_EDY[OutputNames[0]].shape[1]

            # Find sensitive region
            if UtilMethod == 'LOOCV':
                LCerror = MetaModel.LCerror
                allModifiedLOO = np.zeros((len(old_EDX), len(OutputNames),
                                           nMeasurement))
                for y_idx, y_key in enumerate(OutputNames):
                    for idx, key in enumerate(LCerror[y_key].keys()):
                        allModifiedLOO[:, y_idx, idx] = abs(
                            LCerror[y_key][key])

                ExploitScore = np.max(np.max(allModifiedLOO, axis=1), axis=1)

            elif UtilMethod in ['EIGF', 'ALM']:
                # ----- All other in  ['EIGF', 'ALM'] -----
                # Initilize the ExploitScore array
                ExploitScore = np.zeros((len(old_EDX), len(OutputNames)))

                # Split the candidates in groups for multiprocessing
                if explore_method != 'Voronoi':
                    split_cand = np.array_split(allCandidates,
                                                n_cand_groups,
                                                axis=0)
                    goodSampleIdx = range(n_cand_groups)
                else:
                    # Find indices of the Vornoi cells with samples
                    goodSampleIdx = []
                    for idx in range(len(explore.closest_points)):
                        if len(explore.closest_points[idx]) != 0:
                            goodSampleIdx.append(idx)
                    split_cand = explore.closest_points

                # Split the candidates in groups for multiprocessing
                args = []
                for index in goodSampleIdx:
                    args.append((exploit_method, split_cand[index], index,
                                 sigma2, var))

                # Multiprocessing
                pool = multiprocessing.Pool(multiprocessing.cpu_count())
                # With Pool.starmap_async()
                results = pool.starmap_async(self.run_util_func, args).get()

                # Close the pool
                pool.close()
                # out = map(self.run_util_func,
                #           [exploit_method]*len(goodSampleIdx),
                #           split_cand,
                #           range(len(goodSampleIdx)),
                #           [sigma2] * len(goodSampleIdx),
                #           [var] * len(goodSampleIdx)
                #           )
                # results = list(out)

                # Retrieve the results and append them
                if explore_method == 'Voronoi':
                    ExploitScore = [np.mean(results[k][1]) for k in
                                    range(len(goodSampleIdx))]
                else:
                    ExploitScore = np.concatenate(
                        [results[k][1] for k in range(len(goodSampleIdx))])

            else:
                raise NameError('The requested utility function is not '
                                'available.')

            # print("ExploitScore:\n", ExploitScore)

            # find an optimal point subset to add to the initial design by
            # maximization of the utility score and taking care of NaN values
            # Total score
            # Normalize U_J_d
            ExploitScore = ExploitScore / np.sum(ExploitScore)
            totalScore = exploit_w * ExploitScore
            totalScore += explore_w * scoreExploration

            temp = totalScore.copy()
            sorted_idxtotalScore = np.argsort(temp, axis=0)[::-1]
            bestIdx = sorted_idxtotalScore[:n_new_samples]

            Xnew = np.zeros((n_new_samples, ndim))
            if explore_method != 'Voronoi':
                Xnew = allCandidates[bestIdx]
            else:
                for i, idx in enumerate(bestIdx.flatten()):
                    X_can = explore.closest_points[idx]
                    # plotter(self.ExpDesign.X, X_can, explore_method,
                    # scoreExploration=None)

                    # Calculate the maxmin score for the region of interest
                    newSamples, maxminScore = explore.get_mc_samples(X_can)

                    # select the requested number of samples
                    Xnew[i] = newSamples[np.argmax(maxminScore)]

        elif exploit_method == 'alphabetic':
            # ------- EXPLOITATION: ALPHABETIC -------
            Xnew = self.util_AlphOptDesign(allCandidates, var)

        elif exploit_method == 'Space-filling':
            # ------- EXPLOITATION: SPACE-FILLING -------
            totalScore = scoreExploration

            # ------- Select the best candidate -------
            # find an optimal point subset to add to the initial design by
            # maximization of the utility score and taking care of NaN values
            temp = totalScore.copy()
            temp[np.isnan(totalScore)] = -np.inf
            sorted_idxtotalScore = np.argsort(temp)[::-1]

            # select the requested number of samples
            Xnew = allCandidates[sorted_idxtotalScore[:n_new_samples]]

        else:
            raise NameError('The requested design method is not available.')

        print("\n")
        print("\nRun No. {}:".format(old_EDX.shape[0]+1))
        print("Xnew:\n", Xnew)
        gc.collect()

        return Xnew, None

    # -------------------------------------------------------------------------
    def util_AlphOptDesign(self, candidates, var='D-Opt'):
        """
        Enriches the Experimental design with the requested alphabetic
        criterion based on exploring the space with number of sampling points.

        Ref: Hadigol, M., & Doostan, A. (2018). Least squares polynomial chaos
        expansion: A review of sampling strategies., Computer Methods in
        Applied Mechanics and Engineering, 332, 382-407.

        Arguments
        ---------
        NCandidate : int
            Number of candidate points to be searched

        var : string
            Alphabetic optimality criterion

        Returns
        -------
        X_new : array of shape (1, n_params)
            The new sampling location in the input space.
        """
        MetaModelOrig = self
        Model = self.Model
        n_new_samples = MetaModelOrig.ExpDesign.n_new_samples
        NCandidate = candidates.shape[0]

        # TODO: Loop over outputs
        OutputName = Model.Output.names[0]

        # To avoid changes ub original aPCE object
        MetaModel = deepcopy(MetaModelOrig)

        # Old Experimental design
        oldExpDesignX = MetaModel.ExpDesign.X

        # TODO: Only one psi can be selected.
        # Suggestion: Go for the one with the highest LOO error
        Scores = list(MetaModel.score_dict[OutputName].values())
        ModifiedLOO = [1-score for score in Scores]
        outIdx = np.argmax(ModifiedLOO)

        # Initialize Phi to save the criterion's values
        Phi = np.zeros((NCandidate))

        BasisIndices = MetaModelOrig.basis_dict[OutputName]["y_"+str(outIdx+1)]
        P = len(BasisIndices)

        # ------ Old Psi ------------
        univ_p_val = MetaModelOrig.univ_basis_vals(oldExpDesignX)
        Psi = MetaModelOrig.create_psi(BasisIndices, univ_p_val)

        # ------ New candidates (Psi_c) ------------
        # Assemble Psi_c
        univ_p_val_c = self.univ_basis_vals(candidates)
        Psi_c = self.create_psi(BasisIndices, univ_p_val_c)

        for idx in range(NCandidate):

            # Include the new row to the original Psi
            Psi_cand = np.vstack((Psi, Psi_c[idx]))

            # Information matrix
            PsiTPsi = np.dot(Psi_cand.T, Psi_cand)
            M = PsiTPsi / (len(oldExpDesignX)+1)

            if np.linalg.cond(PsiTPsi) > 1e-12 \
               and np.linalg.cond(PsiTPsi) < 1 / sys.float_info.epsilon:
                # faster
                invM = linalg.solve(M, sparse.eye(PsiTPsi.shape[0]).toarray())
            else:
                # stabler
                invM = np.linalg.pinv(M)

            # ---------- Calculate optimality criterion ----------
            # Optimality criteria according to Section 4.5.1 in Ref.

            # D-Opt
            if var == 'D-Opt':
                Phi[idx] = (np.linalg.det(invM)) ** (1/P)

            # A-Opt
            elif var == 'A-Opt':
                Phi[idx] = np.trace(invM)

            # K-Opt
            elif var == 'K-Opt':
                Phi[idx] = np.linalg.cond(M)

            else:
                raise Exception('The optimality criterion you requested has '
                      'not been implemented yet!')

        # find an optimal point subset to add to the initial design
        # by minimization of the Phi
        sorted_idxtotalScore = np.argsort(Phi)

        # select the requested number of samples
        Xnew = candidates[sorted_idxtotalScore[:n_new_samples]]

        return Xnew

    # -------------------------------------------------------------------------
    def __normpdf(self, y_hat_pce, std_pce, obs_data, total_sigma2s,
                  rmse=None):

        Model = self.Model
        likelihoods = 1.0

        # Loop over the outputs
        for idx, out in enumerate(Model.Output.names):

            # (Meta)Model Output
            nsamples, nout = y_hat_pce[out].shape

            # Prepare data and remove NaN
            try:
                data = obs_data[out].values[~np.isnan(obs_data[out])]
            except AttributeError:
                data = obs_data[out][~np.isnan(obs_data[out])]

            # Prepare sigma2s
            non_nan_indices = ~np.isnan(total_sigma2s[out])
            tot_sigma2s = total_sigma2s[out][non_nan_indices][:nout].values

            # Surrogate error if valid dataset is given.
            if rmse is not None:
                tot_sigma2s += rmse[out]**2

            likelihoods *= stats.multivariate_normal.pdf(
                y_hat_pce[out], data, np.diag(tot_sigma2s),
                allow_singular=True)
        self.Likelihoods = likelihoods

        return likelihoods

    # -------------------------------------------------------------------------
    def __corr_factor_BME(self, obs_data, total_sigma2s, logBME):
        """
        Calculates the correction factor for BMEs.
        """
        MetaModel = self.MetaModel
        samples = MetaModel.ExpDesign.X  # valid_samples
        model_outputs = MetaModel.ExpDesign.Y  # valid_model_runs
        Model = MetaModel.ModelObj
        n_samples = samples.shape[0]

        # Extract the requested model outputs for likelihood calulation
        output_names = Model.Output.names

        # TODO: Evaluate MetaModel on the experimental design and ValidSet
        OutputRS, stdOutputRS = MetaModel.eval_metamodel(samples=samples)

        logLik_data = np.zeros((n_samples))
        logLik_model = np.zeros((n_samples))
        # Loop over the outputs
        for idx, out in enumerate(output_names):

            # (Meta)Model Output
            nsamples, nout = model_outputs[out].shape

            # Prepare data and remove NaN
            try:
                data = obs_data[out].values[~np.isnan(obs_data[out])]
            except AttributeError:
                data = obs_data[out][~np.isnan(obs_data[out])]

            # Prepare sigma2s
            non_nan_indices = ~np.isnan(total_sigma2s[out])
            tot_sigma2s = total_sigma2s[out][non_nan_indices][:nout]

            # Covariance Matrix
            covMatrix_data = np.diag(tot_sigma2s)

            for i, sample in enumerate(samples):

                # Simulation run
                y_m = model_outputs[out][i]

                # Surrogate prediction
                y_m_hat = OutputRS[out][i]

                # CovMatrix with the surrogate error
                # covMatrix = np.diag(stdOutputRS[out][i]**2)
                covMatrix = np.diag((y_m-y_m_hat)**2)
                covMatrix = np.diag(
                    np.mean((model_outputs[out]-OutputRS[out]), axis=0)**2
                    )

                # Compute likelilhood output vs data
                logLik_data[i] += self.__logpdf(
                    y_m_hat, data, covMatrix_data
                    )

                # Compute likelilhood output vs surrogate
                logLik_model[i] += self.__logpdf(y_m_hat, y_m, covMatrix)

        # Weight
        logLik_data -= logBME
        weights = np.exp(logLik_model+logLik_data)

        return np.log(np.mean(weights))

    # -------------------------------------------------------------------------
    def __logpdf(self, x, mean, cov):
        """
        computes the likelihood based on a multivariate normal distribution.

        Parameters
        ----------
        x : TYPE
            DESCRIPTION.
        mean : array_like
            Observation data.
        cov : 2d array
            Covariance matrix of the distribution.

        Returns
        -------
        log_lik : float
            Log likelihood.

        """
        n = len(mean)
        L = linalg.cholesky(cov, lower=True)
        beta = np.sum(np.log(np.diag(L)))
        dev = x - mean
        alpha = dev.dot(linalg.cho_solve((L, True), dev))
        log_lik = -0.5 * alpha - beta - n / 2. * np.log(2 * np.pi)

        return log_lik

    # -------------------------------------------------------------------------
    def __posteriorPlot(self, posterior, par_names, key):

        # Initialization
        newpath = (r'Outputs_SeqPosteriorComparison/posterior')
        os.makedirs(newpath, exist_ok=True)

        bound_tuples = self.MetaModel.bound_tuples
        n_params = len(par_names)
        font_size = 40
        if n_params == 2:

            figPosterior, ax = plt.subplots(figsize=(15, 15))

            sns.kdeplot(x=posterior[:, 0], y=posterior[:, 1],
                        fill=True, ax=ax, cmap=plt.cm.jet,
                        clip=bound_tuples)
            # Axis labels
            plt.xlabel(par_names[0], fontsize=font_size)
            plt.ylabel(par_names[1], fontsize=font_size)

            # Set axis limit
            plt.xlim(bound_tuples[0])
            plt.ylim(bound_tuples[1])

            # Increase font size
            plt.xticks(fontsize=font_size)
            plt.yticks(fontsize=font_size)

            # Switch off the grids
            plt.grid(False)

        else:
            import corner
            figPosterior = corner.corner(posterior, labels=par_names,
                                         title_fmt='.2e', show_titles=True,
                                         title_kwargs={"fontsize": 12})

        figPosterior.savefig(f'./{newpath}/{key}.pdf', bbox_inches='tight')
        plt.close()

        # Save the posterior as .npy
        np.save(f'./{newpath}/{key}.npy', posterior)

        return figPosterior

    # -------------------------------------------------------------------------
    def __hellinger_distance(self, P, Q):
        """
        Hellinger distance between two continuous distributions.

        The maximum distance 1 is achieved when P assigns probability zero to
        every set to which Q assigns a positive probability, and vice versa.
        0 (identical) and 1 (maximally different)

        Parameters
        ----------
        P : array
            Reference likelihood.
        Q : array
            Estimated likelihood.

        Returns
        -------
        float
            Hellinger distance of two distributions.

        """
        mu1 = P.mean()
        Sigma1 = np.std(P)

        mu2 = Q.mean()
        Sigma2 = np.std(Q)

        term1 = np.sqrt(2*Sigma1*Sigma2 / (Sigma1**2 + Sigma2**2))

        term2 = np.exp(-.25 * (mu1 - mu2)**2 / (Sigma1**2 + Sigma2**2))

        H_squared = 1 - term1 * term2

        return np.sqrt(H_squared)

    # -------------------------------------------------------------------------
    def __BME_Calculator(self, MetaModel, obs_data, sigma2Dict, rmse=None):
        """
        This function computes the Bayesian model evidence (BME) via Monte
        Carlo integration.

        """
        # Initializations
        valid_likelihoods = MetaModel.valid_likelihoods

        post_snapshot = MetaModel.ExpDesign.post_snapshot
        if post_snapshot or len(valid_likelihoods) != 0:
            newpath = (r'Outputs_SeqPosteriorComparison/likelihood_vs_ref')
            os.makedirs(newpath, exist_ok=True)

        SamplingMethod = 'random'
        MCsize = 10000
        ESS = 0

        # Estimation of the integral via Monte Varlo integration
        while (ESS > MCsize) or (ESS < 1):

            # Generate samples for Monte Carlo simulation
            X_MC = MetaModel.ExpDesign.generate_samples(
                MCsize, SamplingMethod
                )

            # Monte Carlo simulation for the candidate design
            m_1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
            Y_MC, std_MC = MetaModel.eval_metamodel(samples=X_MC)
            m_2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
            print(f"\nMemory eval_metamodel in BME: {m_2-m_1:.2f} MB")

            # Likelihood computation (Comparison of data and
            # simulation results via PCE with candidate design)
            Likelihoods = self.__normpdf(
                Y_MC, std_MC, obs_data, sigma2Dict, rmse
                )

            # Check the Effective Sample Size (1000<ESS<MCsize)
            ESS = 1 / np.sum(np.square(Likelihoods/np.sum(Likelihoods)))

            # Enlarge sample size if it doesn't fulfill the criteria
            if (ESS > MCsize) or (ESS < 1):
                print(f'ESS={ESS} MC size should be larger.')
                MCsize *= 10
                ESS = 0

        # Rejection Step
        # Random numbers between 0 and 1
        unif = np.random.rand(1, MCsize)[0]

        # Reject the poorly performed prior
        accepted = (Likelihoods/np.max(Likelihoods)) >= unif
        X_Posterior = X_MC[accepted]

        # ------------------------------------------------------------
        # --- Kullback-Leibler Divergence & Information Entropy ------
        # ------------------------------------------------------------
        # Prior-based estimation of BME
        logBME = np.log(np.nanmean(Likelihoods))

        # TODO: Correction factor
        # log_weight = self.__corr_factor_BME(obs_data, sigma2Dict, logBME)

        # Posterior-based expectation of likelihoods
        postExpLikelihoods = np.mean(np.log(Likelihoods[accepted]))

        # Posterior-based expectation of prior densities
        postExpPrior = np.mean(
            np.log(MetaModel.ExpDesign.JDist.pdf(X_Posterior.T))
            )

        # Calculate Kullback-Leibler Divergence
        # KLD = np.mean(np.log(Likelihoods[Likelihoods!=0])- logBME)
        KLD = postExpLikelihoods - logBME

        # Information Entropy based on Entropy paper Eq. 38
        infEntropy = logBME - postExpPrior - postExpLikelihoods

        # If post_snapshot is True, plot likelihood vs refrence
        if post_snapshot or len(valid_likelihoods) != 0:
            # Hellinger distance
            ref_like = np.log(valid_likelihoods[valid_likelihoods > 0])
            est_like = np.log(Likelihoods[Likelihoods > 0])
            distHellinger = self.__hellinger_distance(ref_like, est_like)

            idx = len([name for name in os.listdir(newpath) if 'Likelihoods_'
                       in name and os.path.isfile(os.path.join(newpath, name))])
            fig, ax = plt.subplots()
            try:
                sns.kdeplot(np.log(valid_likelihoods[valid_likelihoods > 0]),
                            shade=True, color="g", label='Ref. Likelihood')
                sns.kdeplot(np.log(Likelihoods[Likelihoods > 0]), shade=True,
                            color="b", label='Likelihood with PCE')
            except:
                pass

            text = f"Hellinger Dist.={distHellinger:.3f}\n logBME={logBME:.3f}"
            "\n DKL={KLD:.3f}"

            plt.text(0.05, 0.75, text, bbox=dict(facecolor='wheat',
                                                 edgecolor='black',
                                                 boxstyle='round,pad=1'),
                     transform=ax.transAxes)

            fig.savefig(f'./{newpath}/Likelihoods_{idx}.pdf',
                        bbox_inches='tight')
            plt.close()

        else:
            distHellinger = 0.0

        # Bayesian inference with Emulator only for 2D problem
        if post_snapshot and MetaModel.n_params == 2 and not idx % 5:
            from bayes_inference.bayes_inference import BayesInference
            from bayes_inference.discrepancy import Discrepancy
            import pandas as pd
            BayesOpts = BayesInference(MetaModel)
            BayesOpts.emulator = True
            BayesOpts.plot_post_pred = False

            # Select the inference method
            import emcee
            BayesOpts.inference_method = "MCMC"
            # Set the MCMC parameters passed to self.mcmc_params
            BayesOpts.mcmc_params = {
                'n_steps': 1e5,
                'n_walkers': 30,
                'moves': emcee.moves.KDEMove(),
                'verbose': False
                }

            # ----- Define the discrepancy model -------
            obs_data = pd.DataFrame(obs_data, columns=self.Model.Output.names)
            BayesOpts.measurement_error = obs_data

            # # -- (Option B) --
            DiscrepancyOpts = Discrepancy('')
            DiscrepancyOpts.type = 'Gaussian'
            DiscrepancyOpts.parameters = obs_data**2
            BayesOpts.Discrepancy = DiscrepancyOpts
            # Start the calibration/inference
            Bayes_PCE = BayesOpts.create_inference()
            X_Posterior = Bayes_PCE.posterior_df.values

        # Clean up
        del Y_MC, std_MC
        gc.collect()

        return (logBME, KLD, X_Posterior, Likelihoods, distHellinger)

    # -------------------------------------------------------------------------
    def __validError(self, MetaModel):

        # MetaModel = self.MetaModel
        Model = MetaModel.ModelObj
        OutputName = Model.Output.names

        # Extract the original model with the generated samples
        valid_samples = MetaModel.valid_samples
        valid_model_runs = MetaModel.valid_model_runs

        # Run the PCE model with the generated samples
        m_1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        valid_PCE_runs, valid_PCE_std = MetaModel.eval_metamodel(samples=valid_samples)
        m_2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        print(f"\nMemory eval_metamodel: {m_2-m_1:.2f} MB")

        rms_error = {}
        valid_error = {}
        # Loop over the keys and compute RMSE error.
        for key in OutputName:
            rms_error[key] = mean_squared_error(
                valid_model_runs[key], valid_PCE_runs[key],
                multioutput='raw_values',
                sample_weight=None,
                squared=False)

            # Validation error
            valid_error[key] = (rms_error[key]**2)
            valid_error[key] /= np.var(valid_model_runs[key], ddof=1, axis=0)

            # Print a report table
            print("\n>>>>> Updated Errors of {} <<<<<".format(key))
            print("\nIndex  |  RMSE   |  Validation Error")
            print('-'*35)
            print('\n'.join(f'{i+1}  |  {k:.3e}  |  {j:.3e}' for i, (k, j)
                            in enumerate(zip(rms_error[key],
                                             valid_error[key]))))

        return rms_error, valid_error

    # -------------------------------------------------------------------------
    def __error_Mean_Std(self):

        MetaModel = self.MetaModel
        # Extract the mean and std provided by user
        df_MCReference = MetaModel.ModelObj.mc_reference

        # Compute the mean and std based on the MetaModel
        pce_means, pce_stds = self._compute_pce_moments(MetaModel)

        # Compute the root mean squared error
        for output in MetaModel.ModelObj.Output.names:

            # Compute the error between mean and std of MetaModel and OrigModel
            RMSE_Mean = mean_squared_error(
                df_MCReference['mean'], pce_means[output], squared=False
                )
            RMSE_std = mean_squared_error(
                df_MCReference['std'], pce_means[output], squared=False
                )

        return RMSE_Mean, RMSE_std

    # -------------------------------------------------------------------------
    def _compute_pce_moments(self, MetaModel):
        """
        Computes the first two moments using the PCE-based meta-model.

        Returns
        -------
        pce_means: dict
            The first moment (mean) of the surrogate.
        pce_stds: dict
            The second moment (standard deviation) of the surrogate.

        """
        outputs = MetaModel.ModelObj.Output.names
        pce_means_b = {}
        pce_stds_b = {}

        # Loop over bootstrap iterations
        for b_i in range(MetaModel.n_bootstrap_itrs):
            # Loop over the metamodels
            coeffs_dicts = MetaModel.coeffs_dict[f'b_{b_i+1}'].items()
            means = {}
            stds = {}
            for output, coef_dict in coeffs_dicts:

                pce_mean = np.zeros((len(coef_dict)))
                pce_var = np.zeros((len(coef_dict)))

                for index, values in coef_dict.items():
                    idx = int(index.split('_')[1]) - 1
                    coeffs = MetaModel.coeffs_dict[f'b_{b_i+1}'][output][index]

                    # Mean = c_0
                    if coeffs[0] != 0:
                        pce_mean[idx] = coeffs[0]
                    else:
                        clf_poly = MetaModel.clf_poly[f'b_{b_i+1}'][output]
                        pce_mean[idx] = clf_poly[index].intercept_
                    # Var = sum(coeffs[1:]**2)
                    pce_var[idx] = np.sum(np.square(coeffs[1:]))

                # Save predictions for each output
                if MetaModel.dim_red_method.lower() == 'pca':
                    PCA = MetaModel.pca[f'b_{b_i+1}'][output]
                    means[output] = PCA.mean_ + np.dot(
                        pce_mean, PCA.components_)
                    stds[output] = np.sqrt(np.dot(pce_var,
                                                  PCA.components_**2))
                else:
                    means[output] = pce_mean
                    stds[output] = np.sqrt(pce_var)

            # Save predictions for each bootstrap iteration
            pce_means_b[b_i] = means
            pce_stds_b[b_i] = stds

        # Change the order of nesting
        mean_all = {}
        for i in sorted(pce_means_b):
            for k, v in pce_means_b[i].items():
                if k not in mean_all:
                    mean_all[k] = [None] * len(pce_means_b)
                mean_all[k][i] = v
        std_all = {}
        for i in sorted(pce_stds_b):
            for k, v in pce_stds_b[i].items():
                if k not in std_all:
                    std_all[k] = [None] * len(pce_stds_b)
                std_all[k][i] = v

        # Back transformation if PCA is selected.
        pce_means, pce_stds = {}, {}
        for output in outputs:
            pce_means[output] = np.mean(mean_all[output], axis=0)
            pce_stds[output] = np.mean(std_all[output], axis=0)

        return pce_means, pce_stds
