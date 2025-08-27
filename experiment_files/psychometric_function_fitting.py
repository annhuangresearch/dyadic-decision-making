from ddm import Fittable, Fitted
from ddm.models import DriftConstant, NoiseConstant, BoundConstant, OverlayNonDecision, ICPointSourceCenter
from ddm import Model
from ddm.functions import fit_adjust_model, display_model
import pandas as pd
from ddm import Sample
import ddm.models
from ddm import Fittable, Fitted
from ddm.models import LossRobustBIC
from ddm import Model
from psychopy import data
from ddm.models import DriftConstant, NoiseConstant, BoundConstant, OverlayNonDecision, ICPointSourceCenter
from ddm.functions import fit_adjust_model, display_model
import matplotlib.pyplot as plt
import numpy as np
from ddm import LossFunction
import matplotlib
matplotlib.use('Agg')

# create drift class such that drift rate linearly depends on coherence condition
class DriftCoherence(ddm.models.Drift):
    """
    A custom PyDDM coherence object to make the effective drift rate be a product of coherence and the drift rate parameter.
    This is necessary to follow the procedure in Palmer et al 2005 (which Murphy et al 2014 adopted)
    """

    name = "Drift depends linearly on coherence"
    required_parameters = ["driftcoh"] # <-- Parameters we want to include in the model
    required_conditions = ["coherence"] # <-- Task parameters ("conditions"). Should be the same name as in the sample.

    # We must always define the get_drift function, which is used to compute the instantaneous value of drift.
    def get_drift(self, conditions, **kwargs):
        return self.driftcoh * conditions['coherence']


### Define the psychometric function and its inverse
def psychometric_function(coherence, bound, drift_rate, offset=0):
    """
    Computes the mean correctness associated with the combination (coherence, bound, drift_rate, offset).
    Drift rate and bound form a product which is the effective single parameter of this psychometric function.

    Arguments:
    coherence (float) : Value between 0 and 1 for which to evaluate the psychometric function.
    bound (float) : Parameter of the psychometric function
    drift_rate (float) : Parameter of the psychometric function
    """

    return 1/(1+np.exp(-2*bound*drift_rate*(coherence+offset)))

def psychometric_inverse(requested_accuracy, bound, drift_rate, offset=0):
    """
    Computes the inverse of the psychometric function given the parameters and the accuracy for which to evaluate the psychometric inverse for the associated coherence.

    Arguments:
    requested_accuracy (float) : Value between 0.5 and 1.0
    """
    return -np.log((1/requested_accuracy)-1)/(2*bound*drift_rate) - offset

# function to load csv file(s), merge them and extract correct columns (coherence, rt, correct), filter for >0.1 and <1.5 seconds.
# Return Sample.from_pandas_dataframe .....

def load_data(file_path):
    """
    Loads dataframe from titration (a csv file) and creates pyddm samples from it with coherence as condition.
    """

    df = pd.read_csv(file_path)
    df = df[df['block'] != -2]
    df =  df[df["rt"]<1.5]
    df =  df[df["rt"]>0.1]
    df["correct"] = df["direction"] == df["response"]

    df = df[['correct','coherence','rt']]

    sample = Sample.from_pandas_dataframe(df, rt_column_name ="rt", correct_column_name="correct")

    return sample

def load_combined_data(file_path_titration, file_path_experiment, s1_state=True):
    """
    Loads both the titration csv as well as the main experiment csv and loads it as a sample object for pyddm fitting.

    Arguments:
    file_path_titration (str) : filepath to titration data for the subject (is saved in subject class as the titration_fp attribute).
    file_path_experiment (str) : filepath to the experiment data that has been collected up to this point.
    s1_state (bool)            : Boolean specifying whether it's subject 1's turn or not.
    """
    df_titration = pd.read_csv(file_path_titration)

    df_titration = df_titration[df_titration['block'] != -2]
    df_titration =  df_titration[df_titration["rt"]<1.5]
    df_titration = df_titration[df_titration["rt"]>0.1]
    df_titration["correct"] = df_titration["direction"] == df_titration["response"]
    df_titration = df_titration[['correct','coherence','rt']]

    df_main = pd.read_csv(file_path_experiment)

    df_main = df_main[df_main['block'] != -0.5]
    df_main = df_main[df_main["s1_state"] == s1_state]
    df_main = df_main[df_main["rt"]<1.5]
    df_main = df_main[df_main["rt"]>0.1]
    df_main["correct"] = df_main["direction"] == df_main["response"]
    df_main = df_main[['correct','coherence','rt']]

    # copy main experiment data to make it more important in the ddm fitting
    df_main_2 = df_main
    # slightly change coherence, so pyddm will recognize it as different and treat it specially
    df_main_2["coherence"] = df_main_2["coherence"] + 1e-5

    df_main_3 = df_main
    # slightly change coherence, so pyddm will recognize it as different and treat it specially
    df_main_3["coherence"] = df_main_3["coherence"] + 1.5e-5

    df = pd.concat([df_titration, df_main, df_main_2, df_main_3], axis=0)
    df = df.reset_index()

    sample = Sample.from_pandas_dataframe(df, rt_column_name ="rt", correct_column_name="correct")

    return sample

# Create LossByMeans object
class LossByMeans(LossFunction):
    """
    PyDDM loss object to do exactly what Palmer et al 2005 and Murphy et al 2014 did.
    Computes the mean correctness and mean reaction time for each coherence condition in the samples.
    Then computes the total mean squared error for each condition for (i) mean correctness and (ii) mean reaction time, between data and DDM predictions under the current model parameters.
    """
    name = "Mean RT and accuracy"
    def setup(self, dt, T_dur, **kwargs):
        self.dt = dt
        self.T_dur = T_dur
    def loss(self, model, exponential_accuracy=False):
        sols = self.cache_by_conditions(model)
        MSE = 0
        for comb in self.sample.condition_combinations(required_conditions=self.required_conditions):
            c = frozenset(comb.items())
            s = self.sample.subset(**comb)
            MSE += (sols[c].prob_correct() - s.prob_correct())**2

            if sols[c].prob_correct() > 0:
                weights=None
                MSE += (sols[c].mean_decision_time() - np.average(list(s), weights = weights))**2
        return MSE

# Create ExponentialWeightedLossByMeans object
# class ExponentialWeightedLossByMeans(LossFunction):
#     name = "Mean RT and exponentially weighted accuracy"
#     def setup(self, dt, T_dur, **kwargs):
#         self.dt = dt
#         self.T_dur = T_dur
#     def loss(self, model, exponential_accuracy=True):
#         sols = self.cache_by_conditions(model)
#         MSE = 0
#         for comb in self.sample.condition_combinations(required_conditions=self.required_conditions):
#             c = frozenset(comb.items())
#             s = self.sample.subset(**comb)
#             MSE += (sols[c].prob_correct() - s.prob_correct())**2
#             if sols[c].prob_correct() > 0:
#                 # exponentially weighting the past
#                 weights=None
#                 if exponential_accuracy:
#                     weights = np.exp(np.linspace(-1., 0., len(list(s))))
#                     weights /= weights.sum()
#                     print(len(list(s)))
#
#                 MSE += (sols[c].mean_decision_time() - np.average(list(s), weights = weights))**2
#         return MSE


def fit_ddm_psychometric_function(sample, requested_accuracy, save_plot_to=None):
    """
    Fits a ddm model with PyDDM to the loaded data and computes the coherence threshold for a requested accuracy level. Saves a plot to a filepath.

    Arguments:
    sample : a PyDDM sample object, as obtained from either load_data or load_combined_data.
    requested_accuracy (float) : The desired mean correctness during the experiment.
    save_plot_to (str) : The filepath to save a plot of the psychometric function to.

    Returns:
    threshold (float) : The new coherence value for which the requested accuracy is expected according to the fitted model.
    drift rate (float): One of the two psychometric curve parameters.
    bound (float)     : decision bound of the DDM model (the second psychometric curve parameter)
    """
    loss_function = LossByMeans

    model_fit = Model(name='Proportional Drift Rate Model (fitted)',
                      drift=DriftCoherence(driftcoh=Fittable(minval=1, maxval=25)),
                      noise=NoiseConstant(noise=1),
                      bound=BoundConstant(B=Fittable(minval=0.01, maxval=4)),
                      overlay=OverlayNonDecision(nondectime=Fittable(minval=0, maxval=1)),
                      dx=.001, dt=.01, T_dur=2)

    model_trained = fit_adjust_model(sample, model_fit,
                     fitting_method="differential_evolution",
                     lossfunction=loss_function, verbose=False, verify=False)


    drift_rate = model_trained.get_model_parameters()[0].real
    bound = model_trained.get_model_parameters()[1].real
    non_decision_time = model_trained.get_model_parameters()[2].real

    # estimate 75% threshold
    threshold = psychometric_inverse(requested_accuracy, bound, drift_rate)
    print(threshold)

    if save_plot_to is not None:
        # plot psychometric curve
        coherences = np.linspace(0,1,200)
        accuracies = psychometric_function(coherences, bound, drift_rate)

        fig, ax = plt.subplots(1, 1)
        ax.plot(coherences, accuracies, '-')
        ax.axhline(0.75, linestyle='-', color='orange')
        ax.axvline(threshold, linestyle='-', color='orange')
        plt.title('coherence threshold = %0.3f' % threshold)
        plt.xlabel('Coherence')
        plt.ylabel("Accuracy")
        plt.ylim([0, 1])
        plt.savefig(save_plot_to)

    return threshold, drift_rate, bound
