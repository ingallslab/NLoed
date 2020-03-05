import casadi as cs
import numpy as np
import copy as cp
import scipy as sc

class model:
    """ 
    Add a docstring
    """

    #Moderate:  implement ML fitting
    #           implement data sampling
    #Difficult: implement various cov/bias assesment methods, also (profile) likelihood intervals/plots
    #           add other distributions binomial/bernouli, lognormal, gamma, exponential, weibull etc., negative binomial
    #           implement plotting function (move to utility.py?)
    
    #NOTE: Data/design/experiment objects may need deep copies so internal lists aren't shared??
    #NOTE: do we really need scipy and numpy?
    #names must be unique
    #must enforce ordering of parameters in statistics function

    def __init__(self, observationlist, inputnames, paramnames):
        
        #check for unique names
        if not(len(set(inputnames))  ==  len(inputnames)):
            raise Exception('Model input names must be unique!')
        if not(len(set(paramnames))  ==  len(paramnames)):
            raise Exception('Parameter names must be unique!')
        # extract and store dimensions of the model
        self.NumObserv = len(observationlist)
        self.NumParams = max(observationlist[0][2].size_in(0)) #somewhat unsafe, using max assumes its nx1 or 1xn
        self.NumInputs = max(observationlist[0][2].size_in(1))
        if not(len(set(inputnames))  ==  len(inputnames)):
            raise Exception('Model depends on '+str(self.NumInputs)+' inputs but there are '+str(len(inputnames))+' input names!')
        if not(self.NumParams  ==  len(paramnames)):
            raise Exception('Model depends on '+str(self.NumParams)+' parameters but there are '+str(len(paramnames))+' parameter names!')
        #read names into a dictionary, can be used to link names to index of list functions
        self.InputNameDict = {}
        self.ParamNameDict = {}
        for i in range(self.NumInputs):
            self.InputNameDict[inputnames[i]] = i
        for i in range(self.NumParams):
            self.ParamNameDict[paramnames[i]] = i
        self.ObservNameDict = {}
        #lists to contains needed Casadi functions for evaluation, design and fitting
        self.Dist = []
        self.StatisticModel = []
        self.Model = []
        self.LogLik = []
        self.FIM = []

        #create symbols for parameters and inputs, needed for function defs below
        ParamSymbols = cs.SX.sym('ParamSymbols',self.NumParams)
        InputSymbols = cs.SX.sym('InputSymbols',self.NumInputs)

        for i in range(self.NumObserv):
            Observation = observationlist[i]
            #store the distribution type for later
            self.Dist.append(Observation[1])
            #extract names of observationlist variables
            if not(Observation[0] in self.ObservNameDict):
                self.ObservNameDict[Observation[0]] = i
            else:
                raise Exception('Observation names must be unique!')
            #create a observationlist symbol
            ObervSymbol = cs.SX.sym(Observation[0],1)
            #store the function for the model (links observationlist distribution parameters to the parameters-of-interest)
            self.StatisticModel.append(Observation[2])
            if Observation[1]  == 'Normal':
                #get the distribution statistics
                Mean = Observation[2](ParamSymbols,InputSymbols)[0]
                Variance = Observation[2](ParamSymbols,InputSymbols)[1]
                #create LogLikelihood symbolics and function 
                LogLikSymbol =  -0.5*cs.log(2*cs.pi*Variance) - (ObervSymbol-Mean)**2/(2*Variance)
                self.LogLik.append( cs.Function('ll_'+Observation[0], [ObervSymbol,ParamSymbols,InputSymbols], [LogLikSymbol]) )
                #generate derivatives of distribution parameters, StatisticModel (here Mean and Variance) with respect to parameters-of-interest, Params
                dMean_dParams = cs.jacobian(Mean,ParamSymbols)
                dVariance_dParams = cs.jacobian(Variance,ParamSymbols)
                #create FIM symbolics and function
                FIMSymbol = (dMean_dParams.T @ dMean_dParams)/Variance+(dVariance_dParams.T @ dVariance_dParams)/Variance**2
                self.FIM.append(cs.Function('FIM_'+Observation[0], [ParamSymbols,InputSymbols], [FIMSymbol]) )
            elif Observation[1] == 'Poisson':
                #get the distribution statistic
                Lambda = Observation[2](ParamSymbols,InputSymbols)[0]
                #create a custom casadi function for doing factorials (needed in poisson LogLikelihood and FIM)
                fact = factorial('fact')
                #store the function in the class so it doesn't go out of scope
                self.___factorialFunc = fact
                #create LogLikelihood symbolics and function 
                LogLikSymbol =  ObervSymbol*cs.log(Lambda)+fact(ObervSymbol)-Lambda
                self.LogLik.append( cs.Function('ll_'+Observation[0], [ObervSymbol,ParamSymbols,InputSymbols], [LogLikSymbol]) )
                #generate derivatives of distribution parameters, StatisticModel (here Mean and Variance) with respect to parameters-of-interest, Params
                dLambda_dParams = cs.jacobian(Lambda,ParamSymbols)
                #create FIM symbolics and function
                FIMSymbol = (dLambda_dParams.T @ dLambda_dParams)/Lambda
                self.FIM.append(cs.Function('FIM_'+Observation[0], [ParamSymbols,InputSymbols], [FIMSymbol]) )
            elif Observation[1] == 'Lognormal':    
                print('Not Implemeneted')
            elif Observation[1] == 'Binomial': 
                print('Not Implemeneted')
            elif Observation[1] == 'Exponential': 
                print('Not Implemeneted')
            elif Observation[1] == 'Gamma': 
                print('Not Implemeneted')
            else:
                raise Exception('Unknown Distribution: '+Observation[1])

    def fit(self,datasets,paramstart,paramconstraints=None,opt={'ProfileCIs':False,'ProfilePlots':False}):
        """
        fit the model to a dataset using maximum likelihood and casadi/IPOPT
        """
        #NOTE: add some print statments to provide user with progress status
        #NOTE: could solve multiplex simultaneosly (one big opt problem) or sequentially (more flexible, perhaps slower, leaning towards this for now)

        #NOTE: perhaps allow for bias-reducing penalized likelihood (based on Firth 1993, not sure if generalizes to fully nonlinear problems, seems to use FIM
        #NOTE: allow for parameter constraints to be passed (once FIM supports constraints)

        #NOTE: should (profile) logliklihood CI's ?? plot profiles?
        #NOTE: leave it to user (and show in docs) how to use loglike to get profile liklihood region

        #NOTE: multiplex this, so it fits multiple datasets
        #NOTE: bootstrap CI's/bias very expensive, depends somewhat on larger datasets and not sure how it interacts with our designs (i.e. each bootstrap is non-optimal, heavily replicated design may be okay)
        #            (profile) likelihood: intervals/basins not sure how to return

        #NOTE: add profile likelihood, bootstrap CI's

        if not(isinstance(datasets, list)):
            DesignSet=[[datasets]]
        elif not(isinstance(datasets[0], list)):
            DesignSet=[datasets]
        else:
            DesignSet=datasets

        DesignFitParameterList=[]
        ParamFitSymbols = cs.SX.sym('ParamFitSymbols',self.NumParams)
        for e in range(len(DesignSet)):
            Datasets=DesignSet[e]
            ReplicateFitParameterList=[]
            for r in range(len(Datasets)):
                Data=Datasets[r]
                TotalLogLik=0
                for i in range(len(Data['Inputs'])):
                    InputRow = Data['Inputs'][i]
                    for j in range(self.NumObserv):
                        Observations = Data['Observation'][i][j]
                        for k in range(len(Observations)):
                            TotalLogLik-=self.LogLik[j](Observations[k],ParamFitSymbols,InputRow)

                #NOTE: should be checking solution for convergence, should allow use to pass options to ipopt
                # Create an IPOPT solver for maximum likelihood problem
                IPOPTProblemStructure = {'f': TotalLogLik, 'x': ParamFitSymbols}#, 'g': cs.vertcat(*OptimConstraints)
                IPOPTSolver = cs.nlpsol('solver', 'ipopt', IPOPTProblemStructure,{'ipopt.print_level':0,'print_time':False})
                # Solve the NLP fitting problem with IPOPT call
                #print('Begining optimization...')
                IPOPTSolutionStruct = IPOPTSolver(x0=paramstart)#, lbx=[], ubx=[], lbg=[], ubg=[]
                FitParameters = IPOPTSolutionStruct['x'].full().flatten()
                ReplicateFitParameterList.append(list(FitParameters))

                #NOTE: lots we can do here to speed this up, bates/watts 1988 interpolation of contours, kademan/bates 1990 adaptive profile stepping (derivative of ll and delta theta from last step)
                # if opt['ProfileCIs'] or opt['ProfilePlots']:
                #     TotalLogLikFunc = cs.Function('TotalLogLik_'+str(e)+'_'+str(r), [ParamFitSymbols], [TotalLogLik])
                #     NuisanceParamSymbols=cs.SX.sym('NuisanceParamSymbols',self.NumParams-1)
                #     ConfidenceLevel = 0.95
                #     ChiSquaredLevel = sc.chi2.ppf(ConfidenceLevel, self.NumParams)
                #     LogLikAtEstimate=TotalLogLikFunc(FitParameters)
                #     for p in range(self.NumParams):
                #         NuisanceSubsetList=cs.vertsplit(NuisanceParamSymbols)
                #         NuisanceSubsetList.insert(p,cs.MX(FitParameters[p]))
                #         LeaveOneFixedParamVec=cs.vertcat(*NuisanceSubsetList)
                #         ProfileLikRatioSymbol = 2*(TotalLogLikFunc(LeaveOneFixedParamVec)-LogLikAtEstimate)
                #         ProfileLikRatioFunc = cs.Function('TotalLogLik_'+str(e)+'_'+str(r), [NuisanceParamSymbols], [ProfileLikRatioSymbol])
                           
                #         CurrentRatio=0
                #         StepSize = 0.01 * FitParameters[p]
                #         while CurrentRatio<ChiSquaredLevel:
                #             # Create an IPOPT solver for maximum likelihood problem
                #             IPOPTProblemStructure = {'f': TotalLogLik, 'x': ParamFitSymbols}#, 'g': cs.vertcat(*OptimConstraints)
                #             IPOPTSolver = cs.nlpsol('solver', 'ipopt', IPOPTProblemStructure,{'ipopt.print_level':0,'print_time':False})
                #             # Solve the NLP fitting problem with IPOPT call
                #             #print('Begining optimization...')
                #             IPOPTSolutionStruct = IPOPTSolver(x0=paramstart)#, lbx=[], ubx=[], lbg=[], ubg=[]
                #             FitParameters = IPOPTSolutionStruct['x'].full().flatten()
                #             ReplicateFitParameterList.append(list(FitParameters))



                            # use bisection condition to find F level boundary
                            #store LL value at grid point, endpoints=CI's store in list
                            # plotting: LL profiles per parameter go on diagonal plots, profile traces for each parameter go on off-diagonal lower plots

            DesignFitParameterList.append(ReplicateFitParameterList)
        
        if not(isinstance(datasets, list)):
            return DesignFitParameterList[0][0]
        elif not(isinstance(datasets[0], list)):
            return DesignFitParameterList[0]
        else:
            return DesignFitParameterList
        

    def sample(self,experiments,parameters,replicates=1):
        # generate a data sample fromt the model according to a specific design
        #NOTE: multiplex multiple parameter values??
        #NOTE: actually maybe more important to be able to replicate designs N times

        if not(isinstance(experiments, list)):
            ExperimentList=[experiments]
        else:
            ExperimentList=experiments

        Designset=[]
        for e in range(len(ExperimentList)):
            CurrentExperiment=ExperimentList[e]
            DataFormat=cp.deepcopy(CurrentExperiment)
            del DataFormat['Count']
            DataFormat['Observation']=[]
            Datasets=[]
            for r in range(replicates):
                CurrentData=cp.deepcopy(DataFormat)
                for i in range(len(CurrentExperiment['Inputs'])):
                    InputRow = CurrentExperiment['Inputs'][i]
                    ObservRow=[]
                    for j in range(self.NumObserv):
                        ObservCount = CurrentExperiment['Count'][i][j]
                        Statistics=self.StatisticModel[j](parameters,InputRow)
                        if self.Dist[j] == 'Normal':
                            CurrentDataBlock = np.random.normal(Statistics[0], np.sqrt(Statistics[1]), ObservCount).tolist() 
                        elif self.Dist[j] == 'Poisson':
                            CurrentDataBlock = np.random.poisson(Statistics[0]).tolist() 
                        elif self.Dist[j] == 'Lognormal':
                            print('Not Implemeneted')
                        elif self.Dist[j] == 'Binomial':
                            print('Not Implemeneted')
                        elif self.Dist[j] == 'Exponential':
                            print('Not Implemeneted')
                        elif self.Dist[j] == 'Gamma':
                            print('Not Implemeneted')
                        else:
                            raise Exception('Unknown error encountered selecting observation distribution, contact developers')
                        ObservRow.append(CurrentDataBlock)
                    CurrentData['Observation'].append(ObservRow)
                Datasets.append(CurrentData)
            Designset.append(Datasets)
                
        if not(isinstance(experiments, list)):
            if replicates==1:
                return Designset[0][0]
            else:
                return Designset[0]
        else:
            return Designset

    #NOTE: should maybe rename this
    def evaluate(self):
        #maybe this should move to the design class(??)
        #For D (full cov/bias), Ds (partial cov/bias), T separation using the delta method?! but need two models
        # assess model/design, returns various estimates of cov, bias, confidence regions/intervals
        # no data: asymptotic: covaraince, beale bias, maybe MSE
        #          sigma point: covariance, bias (using mean) (need to figure out how to do sigma for non-normal data), maybe MSE
        #          monte carlo: covariance, bias, MSE
        
        print('Not Implemeneted')
        
    def plots(self):
        #FDS plot, standardized variance (or Ds, bayesian equivlant), residuals
        print('Not Implemeneted')
        #NOTE: maybe add a basic residual computation method for goodness of fit assesment?? Or maybe better show how in tutorial but not here
    
    # UTILITY FUNCTIONS
    def getstatistics(self):
        #NOTE: evaluate model, predict y
        #NOTE: also mabye predict error bars based on par cov or past dataset, delta method vs something based on likelihood CI's??
        print('Not Implemeneted')

    def getFIM(self):
        #NOTE: eval fim at given inputs and dataset
        #NOTE: should this even be here??? how much in model, this isn't data dependent, only design dependent
        print('Not Implemeneted')

    def getloglik(self):
        #eval the logliklihood with given params and dataset
        print('Not Implemeneted')

    def getsensitivity(self):
        #eval observation distribution statistic sensitivities at given input and parameter values
        print('Not Implemeneted')


class factorial(cs.Callback):
    def __init__(self, name, opts = {}):
        cs.Callback.__init__(self)
        self.construct(name, opts)

    # Number of inputs and outputs
    def get_n_in(self): return 1
    def get_n_out(self): return 1

    # Initialize the object
    def init(self):
        print('initializing object')

    # Evaluate numerically
    def eval(self, arg):
        k  =  arg[0]
        cnt = 1
        f = k
        while (k-cnt)>0:
            f = f*(k-cnt)
            cnt = cnt+1
        return [f]


# Full ML fitting, perhaps with penalized likelihood???
# fit assesment, with standardized/weighted residual output, confidence regions via asymptotics (with beale bias), likelihood basins, profile liklihood, sigma point (choose one or maybe two)
# function to generate a prior covariance (that can be fed into design)
# function for easy simulation studies (generate data, with given experiment)