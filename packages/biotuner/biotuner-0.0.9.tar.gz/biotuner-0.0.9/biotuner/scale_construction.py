#!bin/bash
import numpy as np
import matplotlib.pyplot as plt
import sys
from biotuner.biotuner_utils import (nth_root, rebound,
                                     NTET_ratios, scale2frac,
                                     findsubsets, scale_from_pairs)
from biotuner.peaks_extension import consonant_ratios
from biotuner.metrics import (ratios2harmsim, euler,
                              dyad_similarity, metric_denom,
                              tuning_cons_matrix)
from pytuning import create_euler_fokker_scale
import itertools
from collections import Counter
from numpy import linspace, empty, concatenate, log2
from scipy.signal import argrelextrema
from fractions import Fraction
from scipy.stats import norm
import contfrac
sys.setrecursionlimit(120000)


def oct_subdiv(ratio, octave_limit=0.01365, octave=2, n=5):
    '''
    N-TET tuning from Generator Interval
    This function uses a generator interval to suggest
    numbers of steps to divide the octave.

    Parameters
    ----------
    ratio: float
        ratio that corresponds to the generator_interval
        e.g.: by giving the fifth (3/2) as generator interval,
        this function will suggest to subdivide the octave in 12, 53, ...
    octave_limit: float
        Defaults to 0.01365 (Pythagorean comma)
        approximation of the octave corresponding to the acceptable distance
        between the ratio of the generator interval after
        multiple iterations and the octave value.
    octave: int
        Defaults to 2
        value of the octave
    n: int
        Defaults to 5
        number of suggested octave subdivisions

    Returns
    -------
    Octdiv: List (int)
        list of N-TET tunings according to
        the generator interval
    Octvalue: List (float)
        list of the approximations of the octave for each N-TET tuning
    '''
    Octdiv, Octvalue, i = [], [], 1
    ratios = []
    while len(Octdiv) < n:
        ratio_mult = (ratio**i)
        while ratio_mult > octave:
            ratio_mult = ratio_mult/octave

        rescale_ratio = ratio_mult - round(ratio_mult)
        ratios.append(ratio_mult)
        i += 1
        if -octave_limit < rescale_ratio < octave_limit:
            Octdiv.append(i-1)
            Octvalue.append(ratio_mult)
        else:
            continue
    return Octdiv, Octvalue


def compare_oct_div(Octdiv=12, Octdiv2=53, bounds=0.005, octave=2):
    '''
    Function that compares steps for two N-TET tunings
    and returns matching ratios and corresponding degrees

    Parameters
    ----------
    Octdiv: int
        Defaults to 12.
        first N-TET tuning number of steps
    Octdiv2: int
        Defaults to 53.
        second N-TET tuning number of steps
    bounds: float
        Defaults to 0.005
        Maximum distance between one ratio of Octdiv
        and one ratio of Octdiv2 to consider a match
    octave: int
        Defaults to 2
        value of the octave

    Returns
    -------
    avg_ratios: List (float)
        list of ratios corresponding to
        the shared steps in the two N-TET tunings
    shared_steps: List of tuples
        the two elements of each tuple corresponds to the
        tuning steps sharing the same interval in the two N-TET tunings
    '''
    ListOctdiv = []
    ListOctdiv2 = []
    OctdivSum = 1
    OctdivSum2 = 1
    i = 1
    i2 = 1
    while OctdivSum < octave:
        OctdivSum = (nth_root(octave, Octdiv))**i
        i += 1
        ListOctdiv.append(OctdivSum)
    while OctdivSum2 < octave:
        OctdivSum2 = (nth_root(octave, Octdiv2))**i2
        i2 += 1
        ListOctdiv2.append(OctdivSum2)
    shared_steps = []
    avg_ratios = []
    for i, n in enumerate(ListOctdiv):
        for j, harm in enumerate(ListOctdiv2):
            if harm-bounds < n < harm+bounds:
                shared_steps.append((i+1, j+1))
                avg_ratios.append((n+harm)/2)
    return avg_ratios, shared_steps


def multi_oct_subdiv(peaks, max_sub=100, octave_limit=1.01365, octave=2,
                     n_scales=10, cons_limit=0.1):
    '''
    This function uses the most consonant peaks ratios as input of
    oct_subdiv function. Each consonant ratio leads to a list of possible
    octave subdivisions. These lists are compared and optimal octave
    subdivisions are determined.

    Parameters
    ----------
    peaks: List (float)
        Peaks represent local maximum in a spectrum
    max_sub: int
        Defaults to 100.
        Maximum number of intervals in N-TET tuning suggestions.
    octave_limit: float
        Defaults to 1.01365 (Pythagorean comma).
        Approximation of the octave corresponding to the acceptable distance
        between the ratio of the generator interval after
        multiple iterations and the octave value.
    octave: int
        Defaults to 2.
        value of the octave
    n_scales: int
        Defaults to 10.
        Number of N-TET tunings to compute for each generator interval (ratio).

    Returns
    -------
    multi_oct_div: List (int)
        List of octave subdivisions that fit with multiple generator intervals.
    ratios: List (float)
        list of the generator intervals for which at least 1 N-TET tuning
        matches with another generator interval.
    '''
    ratios, cons = consonant_ratios(peaks, cons_limit)
    list_oct_div = []
    for i in range(len(ratios)):
        list_temp, _ = oct_subdiv(ratios[i], octave_limit, octave, n_scales)
        list_oct_div.append(list_temp)
    counts = Counter(list(itertools.chain(*list_oct_div)))
    oct_div_temp = []
    for k, v in counts.items():
        if v > 1:
            oct_div_temp.append(k)
    oct_div_temp = np.sort(oct_div_temp)
    multi_oct_div = []
    for i in range(len(oct_div_temp)):
        if oct_div_temp[i] < max_sub:
            multi_oct_div.append(oct_div_temp[i])
    return multi_oct_div, ratios


def harmonic_tuning(list_harmonics, octave=2, min_ratio=1, max_ratio=2):
    '''
    Generates a tuning based on a list of harmonic positions.

    Parameters
    ----------
    list_harmonics: List (int)
        harmonic positions to use in the scale construction
    octave: int
        value of the period reference
    min_ratio: float
        Defaults to 1.
        Value of the unison.
    max_ratio: float
        Defaults to 2.
        Value of the octave.

    Returns
    -------
    ratios : List (float)
        Generated tuning.
    '''
    ratios = []
    for i in list_harmonics:
        ratios.append(rebound(1*i, min_ratio, max_ratio, octave))
    ratios = list(set(ratios))
    ratios = list(np.sort(np.array(ratios)))
    return ratios


def euler_fokker_scale(intervals, n=1, octave=2):
    '''
    Function that takes as input a series of intervals
    and derives a Euler Fokker Genera scale. Usually,

    Parameters
    ----------
    intervals: List (float)
    n: int
        Defaults to 1
        number of times the interval is used in the scale generation

    Returns
    -------
    ratios : List of float
        Generated tuning.
    '''
    multiplicities = [n for x in intervals]  # Each factor is used once.
    scale = create_euler_fokker_scale(intervals, multiplicities, octave=octave)
    return scale


def generator_interval_tuning(interval=3/2, steps=12, octave=2,
                              harmonic_min=0):
    '''
    Function that takes a generator interval and
    derives a tuning based on its stacking.

    Parameters
    ----------
    interval: float
        Generator interval
    steps: int
        Defaults to 12 (12-TET for interval 3/2)
        Number of steps in the scale
    octave: int
        Defaults to 2
        Value of the octave

    Returns
    -------
    tuning : List of float
        Generated tuning.
    '''
    tuning = []
    for s in range(steps):
        degree = interval**harmonic_min
        while degree > octave:
            degree = degree/octave
        while degree < octave/2:
            degree = degree*octave
        tuning.append(degree)
        harmonic_min += 1
    return sorted(tuning)


def convergents(interval):
    """Return the convergents of the log2 of a ratio.
       The second value represents the number of steps to divide the octave
       while the first value represents the number of octaves up before
       the stacke ratio arrives approximately to the octave value.
       For example, the interval 1.5 will gives [7, 12], which means that
       to approximate the fifth (1.5) in a NTET-tuning, you can divide the
       octave in 12, while stacking 12 fifth will lead to the 7th octave up.

    Parameters
    ----------
    interval : float
        Interval to find convergent.

    Returns
    -------
    convergents : List of lists
        Each sublist corresponds to a pair of convergents.

    """
    value = np.log2(interval)
    convergents = list(contfrac.convergents(value))
    return convergents


# Dissonance curves

def dissmeasure(fvec, amp, model='min'):
    """
    Given a list of partials in fvec, with amplitudes in amp, this routine
    calculates the dissonance by summing the roughness of every sine pair
    based on a model of Plomp-Levelt's roughness curve.
    The older model (model='product') was based on the product of the two
    amplitudes, but the newer model (model='min') is based on the minimum
    of the two amplitudes, since this matches the beat frequency amplitude.

    Parameters
    ----------
    fvec : List
        List of frequency values
    amp : List
        List of amplitude values
    model : str
        Description of parameter `model`.

    Returns
    -------
    D: float
        Dissonance value
    """
    # Sort by frequency
    sort_idx = np.argsort(fvec)
    am_sorted = np.asarray(amp)[sort_idx]
    fr_sorted = np.asarray(fvec)[sort_idx]

    # Used to stretch dissonance curve for different freqs:
    Dstar = 0.24  # Point of maximum dissonance
    S1 = 0.0207
    S2 = 18.96

    C1 = 5
    C2 = -5

    # Plomp-Levelt roughness curve:
    A1 = -3.51
    A2 = -5.75

    # Generate all combinations of frequency components
    idx = np.transpose(np.triu_indices(len(fr_sorted), 1))
    fr_pairs = fr_sorted[idx]
    am_pairs = am_sorted[idx]

    Fmin = fr_pairs[:, 0]
    S = Dstar / (S1 * Fmin + S2)
    Fdif = fr_pairs[:, 1] - fr_pairs[:, 0]

    if model == 'min':
        a = np.amin(am_pairs, axis=1)
    elif model == 'product':
        a = np.prod(am_pairs, axis=1)  # Older model
    else:
        raise ValueError('model should be "min" or "product"')
    SFdif = S * Fdif
    D = np.sum(a * (C1 * np.exp(A1 * SFdif) + C2 * np.exp(A2 * SFdif)))

    return D


def diss_curve(freqs, amps, denom=1000, max_ratio=2, euler_comp=True,
               method='min', plot=True, n_tet_grid=None):
    '''
    This function computes the dissonance curve and related metrics for
    a given set of frequencies (freqs) and amplitudes (amps).

    Parameters
    ----------
    freqs: List (float)
        list of frequencies associated with spectral peaks
    amps: List (float)
        list of amplitudes associated with freqs (must be same lenght)
    denom: int
        Defaults to 1000.
        Highest value for the denominator of each interval
    max_ratio: int
        Defaults to 2.
        Value of the maximum ratio
        Set to 2 for a span of 1 octave
        Set to 4 for a span of 2 octaves
        Set to 8 for a span of 3 octaves
        Set to 2**n for a span of n octaves
    euler: Boolean
        Defaults to True
        When set to True, compute the Euler Gradus Suavitatis
        for the derived scale
    method: str
        {'min', 'product'}
        Defaults to 'min'
        Refer to dissmeasure function for more information.
    plot: boolean
        Defaults to True
        When set to True, a plot of the dissonance curve will be generated
    n_tet_grid: int
        Defaults to None
        When an integer is given, dotted lines will be add to the plot
        at steps of the given N-TET scale

    Returns
    -------
    intervals: List of tuples
        Each tuple corresponds to the numerator and the denominator
        of each scale step ratio
    ratios: List (float)
        list of ratios that constitute the scale
    euler_score: int
        value of consonance of the scale
    diss: float
        value of averaged dissonance of the total curve
    dyad_sims: List (float)
        list of dyad similarities for each ratio of the scale

    '''
    freqs = np.array(freqs)
    r_low = 1
    alpharange = max_ratio
    method = method
    n = 1000
    diss = empty(n)
    a = concatenate((amps, amps))
    for i, alpha in enumerate(linspace(r_low, alpharange, n)):
        f = concatenate((freqs, alpha*freqs))
        d = dissmeasure(f, a, method)
        diss[i] = d
    diss_minima = argrelextrema(diss, np.less)
    intervals = []
    for d in range(len(diss_minima[0])):
        frac = Fraction(diss_minima[0][d]
                        / (n/(max_ratio-1))+1).limit_denominator(denom)
        frac = (frac.numerator, frac.denominator)
        intervals.append(frac)
    intervals.append((2, 1))
    ratios = [i[0]/i[1] for i in intervals]
    dyad_sims = ratios2harmsim(ratios[:-1])
    a = 1
    ratios_euler = [a]+ratios
    ratios_euler = [int(round(num, 2)*1000) for num in ratios]
    euler_score = None
    if euler_comp is True:
        euler_score = euler(*ratios_euler)

        euler_score = euler_score/len(diss_minima)
    else:
        euler_score = 'NaN'

    if plot is True:
        plt.figure(figsize=(14, 6))
        plt.plot(linspace(r_low, alpharange, len(diss)), diss)
        plt.xscale('linear')
        plt.xlim(r_low, alpharange)
        try:
            plt.text(1.9, 1.5, 'Euler = '+str(int(euler_score)),
                     horizontalalignment='center',
                     verticalalignment='center', fontsize=16)
        except:
            pass
        for n, d in intervals:
            plt.axvline(n/d, color='silver')
        # Plot N-TET grid
        if n_tet_grid is not None:
            n_tet = NTET_ratios(n_tet_grid, max_ratio=max_ratio)
            for n in n_tet:
                plt.axvline(n, color='red', linestyle='--')
        # Plot scale ticks
        plt.minorticks_off()
        plt.xticks([n/d for n, d in intervals],
                   ['{}/{}'.format(n, d) for n, d in intervals], fontsize=13)
        plt.yticks(fontsize=13)
        plt.tight_layout()
        plt.show()
    return intervals, ratios, euler_score, np.average(diss), dyad_sims


'''Harmonic Entropy'''


def compute_harmonic_entropy_domain_integral(ratios, ratio_interval,
                                             spread=0.01, min_tol=1e-15):
    """
    Parameters
    ----------
    ratios : List
        Frequency ratios
    ratio_interval : List
        All possible intervals to consider
    spread : float
        Defaults to 0.01
    min_tol : float
        Minimal tolerance
        Defaults to 1e-15

    Returns
    -------
    weight_ratios : List
    HE : float
        Harmonic entropy.

    """
    # The first step is to pre-sort the ratios to speed up computation
    ind = np.argsort(ratios)
    weight_ratios = ratios[ind]

    centers = (weight_ratios[:-1] + weight_ratios[1:]) / 2

    ratio_interval = np.array(ratio_interval)
    N = len(ratio_interval)
    HE = np.zeros(N)
    for i, x in enumerate(ratio_interval):
        P = np.diff(concatenate(([0],
                                 norm.cdf(log2(centers),
                                          loc=log2(x),
                                          scale=spread), [1])))
        ind = P > min_tol
        HE[i] = -np.sum(P[ind] * log2(P[ind]))

    return weight_ratios, HE


def compute_harmonic_entropy_simple_weights(numerators, denominators,
                                            ratio_interval, spread=0.01,
                                            min_tol=1e-15):
    # The first step is to pre-sort the ratios to speed up computation
    ratios = numerators / denominators
    ind = np.argsort(ratios)
    numerators = numerators[ind]
    denominators = denominators[ind]
    weight_ratios = ratios[ind]

    ratio_interval = np.array(ratio_interval)
    N = len(ratio_interval)
    HE = np.zeros(N)
    for i, x in enumerate(ratio_interval):
        P = norm.pdf(log2(weight_ratios),
                     loc=log2(x),
                     scale=spread) / np.sqrt(numerators * denominators)
        ind = P > min_tol
        P = P[ind]
        P /= np.sum(P)
        HE[i] = -np.sum(P * log2(P))

    return weight_ratios, HE


def harmonic_entropy(ratios, res=0.001, spread=0.01, plot_entropy=True,
                     plot_tenney=False, octave=2):
    '''
    Harmonic entropy is a measure of the uncertainty in pitch perception,
    and it provides a physical correlate of tonalness,one aspect of the
    psychoacoustic concept of dissonance (Sethares). High tonalness corresponds
    to low entropy and low tonalness corresponds to high entropy.

    Parameters
    ----------
    ratios: List (float)
        ratios between each pairs of frequency peaks.
    res: float
        Defaults to 0.001
        resolution of the ratio steps.
    spread: float
        Default to 0.01
    plot_entropy: boolean
        Defaults to True
        When set to True, plot the harmonic entropy curve.
    plot_tenney: boolean
        Defaults to False
        When set to True, plot the tenney heights (y-axis)
        across ratios (x-axis).
    octave: int
        Defaults to 2
        Value of reference period.

    Returns
    ----------
    HE_minima: List (float)
        List of ratios corresponding to minima of the harmonic entropy curve
    HE: float
        Value of the averaged harmonic entropy

    '''
    fracs, numerators, denominators = scale2frac(ratios)
    ratios = numerators / denominators
    bendetti_heights = numerators * denominators
    tenney_heights = log2(bendetti_heights)

    ind = np.argsort(tenney_heights)  # sort by Tenney height
    bendetti_heights = bendetti_heights[ind]
    tenney_heights = tenney_heights[ind]
    numerators = numerators[ind]
    denominators = denominators[ind]
    if plot_tenney is True:
        fig = plt.figure(figsize=(10, 4), dpi=150)
        ax = fig.add_subplot(111)
        # ax.scatter(ratios, 2**tenney_heights, s=1)
        ax.scatter(ratios, tenney_heights, s=1, alpha=.2)
        # ax.scatter(ratios[:200], tenney_heights[:200], s=1, color='r')
        plt.show()

    # Next, we need to ensure a distance `d` between adjacent ratios
    M = len(bendetti_heights)
    delta = 0.00001
    indices = np.ones(M, dtype=bool)
    for i in range(M - 2):
        ind = abs(ratios[i + 1:] - ratios[i]) > delta
        indices[i + 1:] = indices[i + 1:] * ind
    bendetti_heights = bendetti_heights[indices]
    tenney_heights = tenney_heights[indices]
    numerators = numerators[indices]
    denominators = denominators[indices]
    ratios = ratios[indices]
    M = len(tenney_heights)
    x_ratios = np.arange(1, octave, res)
    _, HE = compute_harmonic_entropy_domain_integral(ratios,
                                                     x_ratios,
                                                     spread=spread)
    # HE = compute_harmonic_entropy_simple_weights(numerators,
    #                                                denominators,
    #                                                x_ratios, spread=0.01)
    ind = argrelextrema(HE, np.less)
    HE_minima = (x_ratios[ind], HE[ind])
    if plot_entropy is True:
        fig = plt.figure(figsize=(10, 4), dpi=150)
        ax = fig.add_subplot(111)
        ax.plot(x_ratios, HE)
        ax.scatter(HE_minima[0], HE_minima[1], color='k', s=4)
        ax.set_xlim(1, octave)
        plt.show()
    return HE_minima, np.average(HE)


'''Scale reduction'''


def tuning_reduction(tuning, mode_n_steps, function, rounding=4,
                     ratio_type='pos_harm'):
    '''
    Function that reduces the number of steps in a scale according
    to the consonance between pairs of ratios.

    Parameters
    ----------
    tuning : List (float)
        scale to reduce
    mode_n_steps: int
        number of steps of the reduced scale
    function : function
        function used to compute the consonance between pairs of ratios
        Choose between: consonance, dyad_similarity, metric_denom
    rounding : int
        maximum number of decimals for each step
    ratio_type: str
        Default to 'pos_harm'
        choice:
        -'pos_harm':a/b when a>b
        -'sub_harm':a/b when a<b
        -'all': pos_harm + sub_harm

    Returns
    -------
    tuning_consonance : float
        Consonance value of the input tuning.
    mode_out : List
        List of mode intervals.
    mode_consonance : float
        Consonance value of the output mode.
    '''
    tuning_values = []
    mode_values = []
    for index1 in range(len(tuning)):
        for index2 in range(len(tuning)):
            if tuning[index1] != tuning[index2]:  # not include the diagonale
                if ratio_type == 'pos_harm':
                    if tuning[index1] > tuning[index2]:
                        entry = tuning[index1]/tuning[index2]
                        mode_values.append([tuning[index1], tuning[index2]])
                        tuning_values.append(function(entry))
                if ratio_type == 'sub_harm':
                    if tuning[index1] < tuning[index2]:
                        entry = tuning[index1]/tuning[index2]
                        mode_values.append([tuning[index1], tuning[index2]])
                        tuning_values.append(function(entry))
                if ratio_type == 'all':
                    entry = tuning[index1]/tuning[index2]
                    mode_values.append([tuning[index1], tuning[index2]])
                    tuning_values.append(function(entry))
    if function == metric_denom:
        cons_ratios = [x for _, x in sorted(zip(tuning_values, mode_values))]
    else:
        cons_ratios = [x for _, x in sorted(zip(tuning_values,
                                                mode_values))][::-1]
    i = 0
    mode_ = []
    mode_out = []
    while len(mode_out) < mode_n_steps:
        cons_temp = cons_ratios[i]
        mode_.append(cons_temp)
        mode_out_temp = [item for sublist in mode_ for item in sublist]
        mode_out_temp = [np.round(x, rounding) for x in mode_out_temp]
        mode_out = sorted(set(mode_out_temp),
                          key=mode_out_temp.index)[0:mode_n_steps]
        i += 1
    mode_metric = []
    for index1 in range(len(mode_out)):
        for index2 in range(len(mode_out)):
            if mode_out[index1] > mode_out[index2]:
                entry = mode_out[index1]/mode_out[index2]
                mode_metric.append(function(entry))
    tuning_consonance = np.average(tuning_values)
    mode_consonance = np.average(mode_metric)
    return tuning_consonance, mode_out, mode_consonance


def create_mode(tuning, n_steps, function):
    sets = list(findsubsets(tuning, n_steps))
    metric_values = []
    for s in sets:
        _, met = tuning_cons_matrix(s, function)
        metric_values.append(met)
    idx = np.argmax(metric_values)
    mode = sets[idx]
    return mode


def pac_mode(pac_freqs, n, function=dyad_similarity,
             method='subset'):
    """Short summary.

    Parameters
    ----------
    pac_freqs : type
        Description of parameter `pac_freqs`.
    n : type
        Description of parameter `n`.
    function : type
        Description of parameter `function`.
    method : str
        {'pairwise', 'subset'}
    Returns
    -------
    type
        Description of returned object.

    """
    if method == 'pairwise':
        _, mode, _ = tuning_reduction(scale_from_pairs(pac_freqs),
                                      mode_n_steps=n,
                                      function=function)
    if method == 'subset':
        mode = create_mode(scale_from_pairs(pac_freqs),
                           mode_n_steps=n,
                           function=function)
    return sorted(mode)


'''--------------------------MOMENTS OF SYMMETRY---------------------------'''


def tuning_range_to_MOS(frac1, frac2, octave=2, max_denom_in=100,
                        max_denom_out=100):
    """
    Function that takes two ratios a input (boundaries of )
    The mediant corresponds to the interval where
    small and large steps are equal.

    Parameters
    ----------
    frac1 : type
        Description of parameter `frac1`.
    frac2 : type
        Description of parameter `frac2`.
    octave : type
        Description of parameter `octave`.
    max_denom_in : type
        Description of parameter `max_denom_in`.
    max_denom_out : type
        Description of parameter `max_denom_out`.

    Returns
    -------
    tuning_range_to_MOS
        Description of returned object.

    """
    a = Fraction(frac1).limit_denominator(max_denom_in).numerator
    b = Fraction(frac1).limit_denominator(max_denom_in).denominator
    c = Fraction(frac2).limit_denominator(max_denom_in).numerator
    d = Fraction(frac2).limit_denominator(max_denom_in).denominator
    print(a, b, c, d)
    mediant = (a+c)/(b+d)
    mediant_frac = sp.Rational((a+c)/(b+d)).limit_denominator(max_denom_out)
    gen_interval = octave**(mediant)
    gen_interval_frac = sp.Rational(octave**(mediant)).limit_denominator(max_denom_out)
    MOS_signature = [d, b]
    invert_MOS_signature = [b, d]
    return mediant, mediant_frac, gen_interval, gen_interval_frac, MOS_signature, invert_MOS_signature


def stern_brocot_to_generator_interval(ratio, octave=2):
    """
    Converts a fraction in the stern-brocot tree to
    a generator interval for moment of symmetry tunings

    Parameters
    ----------
    ratio : float
        stern-brocot ratio
    octave : float
        Reference period.

    Returns
    -------
    gen_interval : float
        Generator interval

    """
    gen_interval = octave**(ratio)
    return gen_interval


def gen_interval_to_stern_brocot(gen):
    """
    Convert a generator interval to fraction in the stern-brocot tree.

    Parameters
    ----------
    gen : float
        Generator interval.

    Returns
    -------
    root_ratio : float
        Fraction in the stern-brocot tree.

    """
    root_ratio = log2(gen)
    return root_ratio


def horogram_tree_steps(ratio1, ratio2, steps=10, limit=1000):
    ratios_list = [ratio1, ratio2]
    s = 0
    while s < steps:
        ratio3 = horogram_tree(ratio1, ratio2, limit)
        ratios_list.append(ratio3)
        ratio1 = ratio2
        ratio2 = ratio3
        s += 1
    frac_list = [ratio2frac(x) for x in ratios_list]
    return frac_list, ratios_list


def horogram_tree(ratio1, ratio2, limit):
    a = Fraction(ratio1).limit_denominator(limit).numerator
    b = Fraction(ratio1).limit_denominator(limit).denominator
    c = Fraction(ratio2).limit_denominator(limit).numerator
    d = Fraction(ratio2).limit_denominator(limit).denominator
    next_step = (a+c)/(b+d)
    return next_step

def phi_convergent_point(ratio1, ratio2):
    Phi = (1 + 5 ** 0.5) / 2
    a = Fraction(ratio1).limit_denominator(1000).numerator
    b = Fraction(ratio1).limit_denominator(1000).denominator
    c = Fraction(ratio2).limit_denominator(1000).numerator
    d = Fraction(ratio2).limit_denominator(1000).denominator
    convergent_point = (c*Phi+a)/(d*Phi+b)
    return convergent_point


def Stern_Brocot(n, a=0, b=1, c=1, d=1):
    if(a+b+c+d > n):
        return 0
    x=Stern_Brocot(n,a+c,b+d,c,d)
    y=Stern_Brocot(n,a,b,a+c,b+d)
    if(x==0):
        if(y==0):
            return [a+c,b+d]
        else:
            return [a+c]+[b+d]+y
    else:
        if(y==0):
            return [a+c]+[b+d]+x
        else:
            return [a+c]+[b+d]+x+y
