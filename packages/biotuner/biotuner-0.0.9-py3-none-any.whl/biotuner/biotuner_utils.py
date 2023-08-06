#!bin/bash
import numpy as np
import matplotlib.pyplot as plt
import pygame
import pygame.sndarray
import pytuning
import pyACA
from pytuning import *
import scipy.signal
import sympy as sp
import functools
import contfrac
import itertools
import operator
import sys
import bottleneck as bn
import pandas as pd
from scipy.stats import pearsonr
from fractions import Fraction
from functools import reduce
import math
from collections import Counter
from scipy.fftpack import rfft, irfft
from pytuning.tuning_tables import create_scala_tuning
try:
    from pyunicorn.timeseries.surrogates import *
    from pyunicorn.timeseries import RecurrenceNetwork
except ModuleNotFoundError:
    pass
try:
    from scipy.signal import butter, lfilter
except ModuleNotFoundError:
    pass
sys.setrecursionlimit(120000)


"""-----------------------PROPORTION FUNCTIONS----------------------------"""


def compute_peak_ratios(peaks, rebound=True, octave=2, sub=False):
    """This function calculates all the ratios
       (with the possibility to bound them between 1 and 2)
       derived from input peaks.

    Parameters
    ----------
    peaks : List (float)
        Peaks represent local maximum in a spectrum
    rebound : boolean
        Defaults to True. False will output unbounded ratios
    octave : int
        Arbitrary wanted number of octaves. Defaults to 2.
    sub : boolean
        Defaults to False. True will include ratios below the unison (1)

    Returns
    -------
    ratios_final: List
        List of frequency ratios.
    """
    # Iterating through successive peaks
    ratios = []
    peak_ratios_final = []
    for p1 in peaks:
        for p2 in peaks:

            # If a peak of value '0' is present, we skip this ratio computation
            if p1 < 0.1:
                p1 = 0.1
            try:
                ratio_temp = p2 / p1
            except:
                pass

            # When sub is set to False, only ratios with numerators
            # higher than denominators are consider
            if sub is False:
                if ratio_temp < 1:
                    ratio_temp = None
            # Ratios of 1 correspond to a peak divided by itself
            # and are therefore not considered
            if ratio_temp == 1:
                ratio_temp = None
            ratios.append(ratio_temp)

        # I imagine there's a reason why you reinit with array
        peak_ratios = np.array(ratios)
        peak_ratios = [i for i in peak_ratios if i]  # dealing with NaNs ?
        peak_ratios = sorted(list(set(peak_ratios)))
        ratios_final = peak_ratios.copy()

    # If rebound is given, all the ratios are constrained
    # between the unison and the octave
    if rebound is True:
        for peak in peak_ratios:

            # will divide the ratio by the octave until it reaches
            # a value under the octave.
            if peak > octave:
                while peak > octave:
                    peak = peak / octave
                peak_ratios_final.append(peak)
            # will multiply the ratio by the octave until it reaches
            # a value over the unison (1).
            if peak < octave:
                while peak < 1:
                    peak = peak * octave
                peak_ratios_final.append(peak)
        # Preparing output
        peak_ratios_final = np.array(peak_ratios_final)
        peak_ratios_final = [i for i in peak_ratios_final if i]
        ratios_final = sorted(list(set(peak_ratios_final)))
    return ratios_final


def scale2frac(scale, maxdenom=1000):
    """Transforms a scale provided as a list of floats into a list of fractions.

    Parameters
    ----------
    scale : List
        List of floats, typically between 1 and 2, representing scale steps.
    maxdenom : int
        Maximum denominator of the output fractions.

    Returns
    -------
    scale_frac : List
        List of fractions representing scale steps.
    num : array
        Numerators of all fractions.
    den : array
        Denominators of all fractions.

    """
    num = []
    den = []
    scale_frac = []
    for step in scale:
        frac = Fraction(step).limit_denominator(maxdenom)
        frac_ = sp.Rational(step).limit_denominator(maxdenom)
        num.append(frac.numerator)
        den.append(frac.denominator)
        scale_frac.append(frac_)
    return scale_frac, np.array(num), np.array(den)


def ratio2frac(ratio, maxdenom=1000):
    """Trasform a ratio expressed as a float in to a fraction.

    Parameters
    ----------
    ratio : float
        Frequency ratio, typically between 1 and 2.
    maxdenom : type
        Maximum denominator of the output fractions.

    Returns
    -------
    frac : List
        List of 2 int (numerator and denominator).

    """
    frac = Fraction(ratio).limit_denominator(maxdenom)
    num = frac.numerator
    den = frac.denominator
    frac = [num, den]
    return frac


def frac2scale(scale):
    """Transforms a scale expressed in fractions
       into a set of float ratios.

    Parameters
    ----------
    scale : List
        List of fractions.

    Returns
    -------
    scale_ratio : List
        Original scale expressed in float ratios.

    """
    scale_ratio = []
    for step in scale:
        scale_ratio.append(float(step))
    return scale_ratio


def chords_to_ratios(chords, harm_limit=2, spread=True):
    """Transforms series of frequencies expressed in float
       into series of integer ratios.

    Parameters
    ----------
    chords : List of lists
        Each sublist corresponds to a series of frequencies
        expressed in float.
    harm_limit : int
        Defaults to 2
        Maximum harmonic of the lower note below which the higher note
        should fall.
    spread : Boolean
        Defaults to True.
        When set to True, the harm_limit is applied to the previous note.
        When set to False, the harm_limit is applied to the first note.
        When harm_limit == 2, setting the spread to False will contain the
        chords within the span of one octave.

    Returns
    -------
    type
        Description of returned object.

    """
    chords_ratios = []
    chords_ratios_bounded = []
    for chord in chords:
        chord = sorted(chord)
        if harm_limit is not None:
            # allow each note to be within the defined
            # harm_limit of the previous note
            if spread is True:
                for note in range(len(chord)):
                    while chord[note] > chord[note - 1] * harm_limit:
                        chord[note] = chord[note] / 2
            # allow each note to be within the defined
            # harm_limit of the first note
            if spread is False:
                for note in range(len(chord)):
                    while chord[note] > chord[0] * harm_limit:
                        chord[note] = chord[note] / 2
        chord = sorted([np.round(n, 1) for n in chord])
        chord = [int(n * 10) for n in chord]
        gcd_chord = 2  # arbitrary number that is higher than 1
        while gcd_chord > 1:
            gcd_chord = gcd(*chord)
            if gcd_chord > 1:
                chord = [int(note / gcd_chord) for note in chord]
        chord_bounded = [c / chord[0] for c in chord]
        chords_ratios_bounded.append(chord_bounded)
        chords_ratios.append(chord)
    return chords_ratios, chords_ratios_bounded


def NTET_steps(octave, step, NTET):
    """This function computes the ratio associated with a specific step
       of a N-TET scale.

    Parameters
    ----------
    octave : int
        value of the octave
    step : int
        value of the step
    NTET : int
        number of steps in the N-TET scale

    Returns
    -------
    answer : float
        Step value.

    """

    answer = octave ** (step / NTET)
    return answer


def NTET_ratios(n_steps, max_ratio, octave=2):
    """Generate a series of ratios dividing the octave in N equal steps.

    Parameters
    ----------
    n_steps : int
        Number of steps dividing the octave.
    max_ratio : type
        Description of parameter `max_ratio`.
    octave : float
        Defaults to 2.
        Value of the octave (period).

    Returns
    -------
    steps_out : List
        List of steps in decimal numbers.

    """
    steps = []
    for s in range(n_steps):
        steps.append(2 ** (s / n_steps))
    steps_out = []
    for j in range(max_ratio - 1):
        steps_out.append([i + j for i in steps])
    steps_out = sum(steps_out, [])
    return steps_out


def scale_from_pairs(pairs):
    """Transforms each pairs of frequencies to ratios.

    Parameters
    ----------
    pairs : List of lists
        Each sublist is a pair of frequencies.

    Returns
    -------
    scale : List
        Scale steps.

    """
    scale = [rebound((x[1] / x[0])) for x in pairs]
    return scale


def ratios_harmonics(ratios, n_harms=1):
    """Computes the harmonics of ratios in the form of r*n when
       r is the ratio expressed as a float and n is the integer
       representing the harmonic position.

    Parameters
    ----------
    ratios : List
        List of ratios expressed as float.
    n_harms : int
        Number of harmonics to compute.

    Returns
    -------
    ratios_harms : List
        List of original ratios and their harmonics.

    """
    ratios_harms = []
    for h in range(n_harms):
        h += 1
        ratios_harms.append([i * h for i in ratios])
    ratios_harms = [i for sublist in ratios_harms for i in sublist]
    return ratios_harms


def ratios_increments(ratios, n_inc=1):
    """Computes the harmonics of ratios in the form of r**n when
       r is the ratio expressed as a float and n is the integer
       representing the increment (e.g. stacking ratios).

    Parameters
    ----------
    ratios : type
        Description of parameter `ratios`.
    n_inc : type
        Description of parameter `n_inc`.

    Returns
    -------
    ratios_harms : List
        List of original ratios and their harmonics.

    """
    ratios_harms = []
    for h in range(n_inc):
        h += 1
        ratios_harms.append([i**h for i in ratios])
    ratios_harms = [i for sublist in ratios_harms for i in sublist]
    ratios_harms = list(set(ratios_harms))
    return ratios_harms


"""---------------------------LIST MANIPULATION--------------------------"""


def flatten(t):
    """Flattens a list of lists.

    Parameters
    ----------
    t : List of lists

    Returns
    -------
    List
        Flattened list.

    """
    return [item for sublist in t for item in sublist]


def findsubsets(S, m):
    """Find all subsets of m elements in a list.

    Parameters
    ----------
    S : List
        List to find subsets in.
    m : int
        Number of elements in each subset.

    Returns
    -------
    List of lists
        Each sublist represents a subset of the original list.

    """
    return list(set(itertools.combinations(S, m)))


def pairs_most_frequent(pairs, n):
    """Finds the most frequent values in a list of lists of pairs of numbers.

    Parameters
    ----------
    pairs : List of lists
        Each sublist should be a pair of values.
    n : int
        Number of most frequent pairs to keep.

    Returns
    -------
    List of lists
        First sublist corresponds to most frequent first values.
        Second sublist corresponds to most frequent second values.

    """
    drive_freqs = [x[0] for x in pairs]
    signal_freqs = [x[1] for x in pairs]
    drive_dict = {
        k: v for k, v in sorted(Counter(drive_freqs).items(),
                                key=lambda item: item[1])
    }
    max_drive = list(drive_dict)[::-1][0:n]
    signal_dict = {
        k: v for k, v in sorted(Counter(signal_freqs).items(),
                                key=lambda item: item[1])
    }
    max_signal = list(signal_dict)[::-1][0:n]
    return [max_signal, max_drive]


def rebound(x, low=1, high=2, octave=2):
    """Rescale a value within given range.

    Parameters
    ----------
    x : float
        Value to rebound.
    low : int
        Lower bound. Defaults to 1.
    high : int
        Higher bound. Defaults to 2.
    octave : int
        Value of an octave.

    Returns
    -------
    x : float
        Input value rescaled between low and high values.

    """

    while x >= high:
        x = x / octave
    while x <= low:
        x = x * octave
    return x


def rebound_list(x_list, low=1, high=2, octave=2):
    """Rescale a list within given range.

    Parameters
    ----------
    x : list
        List to rebound.
    low : int
        Lower bound. Defaults to 1.
    high : int
        Higher bound. Defaults to 2.
    octave : int
        Value of an octave.

    Returns
    -------
    x : list
        Rescaled list between low and high values.

    """
    return [rebound(x, low, high, octave) for x in x_list]


def sum_list(list):
    """Compute the sum of a list.

    Parameters
    ----------
    list : list
        List of values to sum.

    Returns
    -------
    sum : float
        Sum of the list.

    """
    sum = 0
    for x in list:
        sum += x
    return sum


def compareLists(list1, list2, bounds):
    """Find elements that are closest than bounds value from
       two lists.

    Parameters
    ----------
    list1 : list
        First list.
    list2 : list
        Second list.
    bounds : float
        Maximum value between two elements to assume equivalence.

    Returns
    -------
    matching : array
        Elements that match between the two list (average value of the two
        close elements).
    positions : list
        All indexes of the selected elements combined in one list.
    matching_pos : array (n_matching, 3)
        For each matching, a list of the value and the positions
        in list1 and list2.

    """
    matching = []
    matching_pos = []
    positions = []
    for i, l1 in enumerate(list1):
        for j, l2 in enumerate(list2):
            if l2 - bounds < l1 < l2 + bounds:
                matching.append((l1 + l2) / 2)
                matching_pos.append([(l1 + l2) / 2, i + 1, j + 1])
                positions.append(i + 1)
                positions.append(j + 1)
    matching = np.array(matching)
    matching_pos = np.array(matching_pos)
    ratios_temp = []
    for i in range(len(matching_pos)):
        if matching_pos[i][1] > matching_pos[i][2]:
            ratios_temp.append(matching_pos[i][1] / matching_pos[i][2])
        else:
            ratios_temp.append(matching_pos[i][2] / matching_pos[i][1])
    matching_pos_ratios = np.array(ratios_temp)
    return matching, list(set(positions)), matching_pos, matching_pos_ratios


def top_n_indexes(arr, n):
    """Find the index pairs of maximum values in a 2d array.

    Parameters
    ----------
    arr : ndarray(i, j)
        2d array.
    n : int
        Number of index pairs to return.

    Returns
    -------
    indexes : List of lists
        Each sublist contains the 2 indexes associated with higest values
        of the input array.

    """
    idx = bn.argpartition(arr, arr.size - n, axis=None)[-n:]
    width = arr.shape[1]
    indexes = [divmod(i, width) for i in idx]
    return indexes


def getPairs(peaks):
    """Extract all possible pairs of elements from a list.

    Parameters
    ----------
    peaks : List
        List of values.

    Returns
    -------
    out : List of lists
        Each sublist corresponds to a pair of value.

    """
    peaks_ = peaks.copy()
    out = []
    for i in range(len(peaks_) - 1):
        a = peaks_.pop(i - i)
        for j in peaks_:
            out.append([a, j])
    return out


"""--------------------SIMPLE MATHEMATICAL FUNCTIONS-----------------------"""


def nth_root(num, root):
    """This function computes the nth root of a number.

    Parameters
    ----------
    num : int
        value of the octave
    root : int
        number of steps in the N-TET scale

    Returns
    -------
    answer : float
        nth root.

    """
    answer = num ** (1 / root)
    return answer


def gcd(*numbers):
    """Return the greatest common divisor of the given integers
    The result will have the same sign as the last number given (so that
    when the last number is divided by the result, the result comes out
    positive).

    Parameters
    ----------
    *numbers : List
        List of numbers.

    Returns
    -------
    a : float
        Greated common divisor of the input numbers.

    """

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    return reduce(gcd, numbers)


def reduced_form(*numbers):
    """Return a tuple of numbers which is the reduced form of the input,
       which is a list of integers. Ex: [4, 8, 12, 80] -> [1, 2, 3, 20]

    Parameters
    ----------
    *numbers : list (float)
        List of numbers to reduce.

    Returns
    -------
    reduce : list (int)
        Reduced form of the input.

    """
    reduce = tuple(int(a // gcd(*numbers)) for a in numbers)
    return reduce


def lcm(*numbers):
    """Return the least common multiple of the given integers.

    Parameters
    ----------
    *numbers : list (float)
        List of numbers.

    Returns
    -------
    lcm_ : int
        Least common multiple of the input numbers.

    """
    def lcm(a, b):
        if a == b == 0:
            return 0
        return (a * b) // gcd(a, b)
    lcm_ = reduce(lcm, numbers)
    return lcm_


def prime_factors(n):
    """Return a list of the prime factors of the integer n.
       Don't use this for big numbers; it's a dumb brute-force method.

    Parameters
    ----------
    n : int
        Integer to factorize.

    Returns
    -------
    factors : list
        List of prime factors of n.

    """
    factors = []
    lastresult = n
    while lastresult > 1:
        c = 2
        while lastresult % c > 0:
            c += 1
        factors.append(c)
        lastresult /= c
    return factors


def prime_factor(n):
    """Find the prime number in a list of n numbers.

    Parameters
    ----------
    n : type
        Description of parameter `n`.

    Returns
    -------
    type
        Description of returned object.

    """
    prime = []
    for i in n:
        flag = 0
        if i == 1:
            flag = 1
        for j in range(2, i):
            if i % j == 0:
                flag = 1
                break
        if flag == 0:
            prime.append(i)
    return prime


def contFrac(x, k):
    """Compute the continuous fraction of a value x for k steps.

    Parameters
    ----------
    x : float
        Value to decompose.
    k : int
        Number of steps to go through.

    Returns
    -------
    cf : list
        List of denominators (1/cf[0] + 1/cf[1] ... +1/cf[k]).

    """
    cf = []
    q = math.floor(x)
    cf.append(q)
    x = x - q
    i = 0
    while x != 0 and i < k:
        q = math.floor(1 / x)
        cf.append(q)
        x = 1 / x - q
        i = i + 1
    return cf


"""------------------------------SURROGATES--------------------------------"""


def phaseScrambleTS(ts):
    """Returns a TS: original TS power is preserved; TS phase is shuffled.

    Parameters
    ----------
    ts : 1d array (numDataPoints, )
        Oriinal time series.

    Returns
    -------
    tsr : array (numDataPoints)
        Phase scrabled time series.

    """
    fs = rfft(ts)
    # rfft returns real and imaginary components
    # in adjacent elements of a real array
    pow_fs = fs[1:-1:2] ** 2 + fs[2::2] ** 2
    phase_fs = np.arctan2(fs[2::2], fs[1:-1:2])
    phase_fsr = phase_fs.copy()
    np.random.shuffle(phase_fsr)
    # use broadcasting and ravel to interleave
    # the real and imaginary components.
    # The first and last elements in the fourier array don't have any
    # phase information, and thus don't change
    fsrp = np.sqrt(pow_fs[:, np.newaxis]) * np.c_[np.cos(phase_fsr),
                                                  np.sin(phase_fsr)]
    fsrp = np.r_[fs[0], fsrp.ravel(), fs[-1]]
    tsr = irfft(fsrp)
    return tsr


def AAFT_surrogates(original_data):
    """Return surrogates using the amplitude adjusted Fourier transform
       method.

    Parameters
    ----------
    original_data : 2D array (data, index)
        The original time series.

    Returns
    -------
    rescaled_data : 2D array (surrogate, index)
    """
    #  Create sorted Gaussian reference series
    gaussian = np.random.randn(original_data.shape[0], original_data.shape[1])
    gaussian.sort(axis=1)

    #  Rescale data to Gaussian distribution
    ranks = original_data.argsort(axis=1).argsort(axis=1)
    rescaled_data = np.zeros(original_data.shape)

    for i in range(original_data.shape[0]):
        rescaled_data[i, :] = gaussian[i, ranks[i, :]]

    #  Phase randomize rescaled data
    phase_randomized_data = correlated_noise_surrogates(rescaled_data)

    #  Rescale back to amplitude distribution of original data
    sorted_original = original_data.copy()
    sorted_original.sort(axis=1)

    ranks = phase_randomized_data.argsort(axis=1).argsort(axis=1)

    for i in range(original_data.shape[0]):
        rescaled_data[i, :] = sorted_original[i, ranks[i, :]]

    return rescaled_data


def correlated_noise_surrogates(original_data):
    """
    Return Fourier surrogates.

    Generate surrogates by Fourier transforming the :attr:`original_data`
    time series (assumed to be real valued), randomizing the phases and
    then applying an inverse Fourier transform. Correlated noise surrogates
    share their power spectrum and autocorrelation function with the
    original_data time series.

    .. note::
       The amplitudes are not adjusted here, i.e., the
       individual amplitude distributions are not conserved!
    """
    #  Calculate FFT of original_data time series
    #  The FFT of the original_data data has to be calculated only once,
    #  so it is stored in self._original_data_fft.
    surrogates = np.fft.rfft(original_data, axis=1)
    #  Get shapes
    (N, n_time) = original_data.shape
    len_phase = surrogates.shape[1]

    #  Generate random phases uniformly distributed in the
    #  interval [0, 2*Pi]
    phases = np.random.uniform(low=0, high=2 * np.pi, size=(N, len_phase))

    #  Add random phases uniformly distributed in the interval [0, 2*Pi]
    surrogates *= np.exp(1j * phases)

    #  Calculate IFFT and take the real part, the remaining imaginary part
    #  is due to numerical errors.
    return np.ascontiguousarray(np.real(np.fft.irfft(surrogates,
                                                     n=n_time,
                                                     axis=1)))


""""""


def UnivariateSurrogatesTFT(data_f, MaxIter=1, fc=5):
    """Compute Truncated Fourier Transform of the input data.
       from: https://github.com/narayanps/NolinearTimeSeriesAnalysis/blob/
       master/SurrogateModule.py

    Parameters
    ----------
    data_f : array
        Original signal.
    MaxIter : int
        Defaults to 1.
        Maximum number of iterations.
    fc : int
        Defaults to 5.
        Description of parameter `fc`.

    Returns
    -------
    xsur : array
        Surrogate of the original signal.

    """

    xs = data_f.copy()
    xs.sort()  # sorted amplitude stored
    # amplitude of fourier transform of orig
    pwx = np.abs(np.fft.fft(data_f))
    phi = np.angle(np.fft.fft(data_f))
    Len = phi.shape[0]
    # data_f.shape=(-1,1)
    # random permutation as starting point
    xsur = np.random.permutation(data_f)
    # xsur.shape = (1,-1)
    Fc = np.round(fc * data_f.shape[0])
    for i in range(MaxIter):
        phi_surr = np.angle(np.fft.fft(xsur))
        # print(phi_surr.shape)
        # print(phi.shape)
        phi_surr[1:Fc] = phi[1:Fc]
        phi_surr[Len - Fc + 1: Len] = phi[Len - Fc + 1: Len]
        phi_surr[0] = 0.0
        new_len = int(Len / 2)

        phi_surr[new_len] = 0.0

        fftsurx = pwx * np.exp(1j * phi_surr)
        xoutb = np.real(np.fft.ifft(fftsurx))
        ranks = xoutb.argsort(axis=0)
        xsur[ranks] = xs
    return xsur


"""----------------------SPECTROMORPHOLOGY FUNCIONS------------------------"""


def computeFeatureCl_new(
    afAudioData,
    cFeatureName,
    f_s,
    window=4000,
    overlap=1
     ):
    """Calculate spectromorphological metrics on time series.

    Parameters
    ----------
    afAudioData : array (numDataPoints, )
        Input signal.
    cFeatureName : str
        {'SpectralCentroid', 'SpectralCrestFactor', 'SpectralDecrease',
         'SpectralFlatness', 'SpectralFlux', 'SpectralKurtosis',
         'SpectralMfccs', 'SpectralPitchChroma', 'SpectralRolloff',
         'SpectralSkewness', 'SpectralSlope', 'SpectralSpread',
         'SpectralTonalPowerRatio', 'TimeAcfCoeff', 'TimeMaxAcf',
         'TimePeakEnvelope', 'TimeRms', 'TimeStd', 'TimeZeroCrossingRate'}
    f_s : int
        Sampling frequency.
    window : int
        Length of the moving window in samples.
    overlap : int
        Overlap between each moving window in samples.

    Returns
    -------
    v : array
        Vector of the spectromorphological metric.
    t : array
        Timestamps.
    """
    [v, t] = pyACA.computeFeature(
                   cFeatureName,
                   afAudioData,
                   f_s,
                   None,
                   window,
                   overlap)
    return (v, t)


def EMD_to_spectromorph(
    IMFs,
    sf,
    method="SpectralCentroid",
    window=None,
    overlap=1,
    in_cut=None,
    out_cut=None,
):
    """Calculate spectromorphological metrics on intrinsic mode functions
       derived using Empirical Mode Decomposition.

    Parameters
    ----------
    IMFs : array (nIMFs, numDataPoints)
        Input data.
    sf : int
        Sampling frequency of the original signal.
    method : str
        Defaults to 'SpectralCentroid'.
        {'SpectralCentroid', 'SpectralCrestFactor', 'SpectralDecrease',
         'SpectralFlatness', 'SpectralFlux', 'SpectralKurtosis',
         'SpectralMfccs', 'SpectralPitchChroma', 'SpectralRolloff',
         'SpectralSkewness', 'SpectralSlope', 'SpectralSpread',
         'SpectralTonalPowerRatio', 'TimeAcfCoeff', 'TimeMaxAcf',
         'TimePeakEnvelope', 'TimeRms', 'TimeStd', 'TimeZeroCrossingRate'}
    window : int
        Length of the moving window in samples.
    overlap : int
        Overlap between each moving window in samples.
    in_cut : int
        Number of samples to remove at the beginning.
    out_cut : type
        Number of samples to remove at the end.

    Returns
    -------
    spectro_IMF : (nIMFs, numSpectroPoints)
        Spectromorphological metric for each IMF.

    """
    # remove 0.1 second at the beginning and the end of the signal.
    if in_cut is None:
        in_cut = int(sf / 10)
    if out_cut is None:
        out_cut = int(len(IMFs[0]) - (sf / 10))
    if window is None:
        window = int(sf / 2)
    spectro_IMF = []
    for e in IMFs:
        f, t = computeFeatureCl_new(e, method, sf, window, overlap)
        try:
            spectro_IMF.append(f[0][in_cut:out_cut])
        except:
            spectro_IMF.append(f[in_cut:out_cut])
    spectro_IMF = np.array(spectro_IMF)
    return spectro_IMF


"""-------------------GENERATE AUDIO / SIGNAL PROCESSING--------------------"""


sample_rate = 44100
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


def generate_signal(
    sf, time_end, freqs, amps, show=False, theta=0, color="blue"
     ):
    time = np.arange(0, time_end, 1 / sf)
    sine_tot = []
    for i in range(len(freqs)):
        sinewave = amps[i] * np.sin(2 * np.pi * freqs[i] * time + theta)
        sine_tot.append(sinewave)
    sine_tot = sum_list(sine_tot)
    if show is True:
        ax = plt.gca()
        ax.set_facecolor("xkcd:black")
        plt.plot(time, sine_tot, color=color)
    return sine_tot


def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
    Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = np.pi * 2 / length
    xvalues = np.arange(int(length)) * omega
    onecycle = peak * np.sin(xvalues)
    return np.resize(onecycle, (n_samples,)).astype(np.int16)


def square_wave(hz, peak, duty_cycle=0.5, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
    Defaults to one second.
    """
    t = np.linspace(0, 1, 500 * 440 / hz, endpoint=False)
    wave = scipy.signal.square(2 * np.pi * 5 * t, duty=duty_cycle)
    wave = np.resize(wave, (n_samples,))
    return peak / 2 * wave.astype(np.int16)


def smooth(x, window_len=11, window="hanning"):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: dimension of the smoothing window; should be an odd integer
        window: type of window
                {'flat', 'hanning', 'hamming', 'bartlett', 'blackman'}
                flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    NOTE: length(output) != length(input), to correct this:
          return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """
    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    if window == "flat":  # moving average
        w = np.ones(window_len, "d")
    else:
        w = eval("np." + window + "(window_len)")

    y = np.convolve(w / w.sum(), s, mode="valid")
    return y


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def make_chord(hz, ratios):
    """Make a chord based on a list of frequency ratios."""
    sampling = 2048
    chord = waveform(hz, sampling)
    for r in ratios[1:]:
        chord = sum([chord, sine_wave(hz * r / ratios[0], sampling)])
    return chord


def major_triad(hz):
    return make_chord(hz, [4, 5, 6])


def listen_scale(scale, fund, length):
    print("Scale:", scale)
    scale = [1] + scale
    for s in scale:
        freq = fund * s
        print(freq)
        note = make_chord(freq, [1])
        note = np.ascontiguousarray(np.vstack([note, note]).T)
        sound = pygame.sndarray.make_sound(note)
        sound.play(loops=0, maxtime=0, fade_ms=0)
        pygame.time.wait(int(sound.get_length() * length))


def listen_chords(chords, mult=10, length=500):
    print("Chords:", chords)

    for c in chords:
        c = [i * mult for i in c]
        chord = make_chord(c[0], c[1:])
        chord = np.ascontiguousarray(np.vstack([chord, chord]).T)
        sound = pygame.sndarray.make_sound(chord)
        sound.play(loops=0, maxtime=0, fade_ms=0)
        pygame.time.wait(int(sound.get_length() * length))


"""-----------------------------OTHERS----------------------------------"""


def create_SCL(scale, fname):
    """Save a scale to .scl file.

    Parameters
    ----------
    scale : list
        List of scale steps.
    fname : str
        Name of the saved file.

    """
    table = create_scala_tuning(scale, fname)
    outF = open(fname + ".scl", "w")
    outF.writelines(table)
    outF.close()
    return


def scale_interval_names(scale, reduce=False):
    """Gives the name of intervals in a scale based on PyTuning dictionary.

    Parameters
    ----------
    scale : list
        List of scale steps either in float or fraction form.
    reduce : boolean
        Defaults to False.
        When set to True, output only the steps that match a key
        in the dictionary.

    Returns
    -------
    interval_names : list of lists
        Each sublist contains the scale step and the corresponding
        interval names.

    """
    try:
        type = scale[0].dtype == "float64"
        if type is True:
            scale, _, _ = scale2frac(scale)
    except:
        pass
    interval_names = []
    for step in scale:
        name = pytuning.utilities.ratio_to_name(step)
        if reduce is True and name is not None:
            interval_names.append([step, name])
        if reduce is False:
            interval_names.append([step, name])
    return interval_names


def calculate_pvalues(df, method='pearson'):
    """Calculate the correlation between each column of a DataFrame.

    Parameters
    ----------
    df : DataFrame
        DataFrame of values to compute correlation on.
    method : str
        Defaults to pearson.
        {'pearson', 'spearman'}

    Returns
    -------
    type
        Description of returned object.

    """
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how="outer")
    for r in df.columns:
        for c in df.columns:
            if method == 'pearson':
                pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
            if method == 'spearman':
                pvalues[r][c] = round(spearmanr(df[r], df[c])[1], 4)
    return pvalues


def peaks_to_amps(peaks, freqs, amps, sf):
    """Find the amplitudes of spectral peaks.

    Parameters
    ----------
    peaks : list
        Spectral peaks in Hertz.
    freqs : list
        All centers of frequency bins.
    amps : list
        All amplitudes associated with frequency bins.
    sf : int
        Sampling frequency.

    Returns
    -------
    amps_out : list
        Amplitudes of spectral peaks.

    """
    bin_size = np.round((sf / 2) / len(freqs), 3)
    amps_out = []
    for p in peaks:
        index = int(p / bin_size)
        amp = amps[index]
        amps_out.append(amp)
    return amps_out


def alpha2bands(a):
    """Derive frequency bands for M/EEG analysis based on the alpha peak.
       Boundaries of adjacent frequency bands are derived based on the
       golden ratio, which optimizes the uncoupling of phases between
       frequencies. (see: Klimesch, 2018)

    Parameters
    ----------
    a : float
        Alpha peak in Hertz.

    Returns
    -------
    FREQ_BANDS : List of lists
        Each sublist contains the boundaries of each frequency band.

    """
    np.float(a)
    center_freqs = [a / 4, a / 2, a, a * 2, a * 4]
    FREQ_BANDS = []
    for f in center_freqs:
        down = np.round((f / 2) * 1.618, 1)
        up = np.round((f * 2) * 0.618, 1)
        band = [down, up]
        FREQ_BANDS.append(band)
    return FREQ_BANDS


def __get_norm(norm):
    if norm == 0 or norm is None:
        return None, None
    else:
        try:
            norm1, norm2 = norm
        except TypeError:
            norm1 = norm2 = norm
        return norm1, norm2


def __freq_ind(freq, f0):
    try:
        return [np.argmin(np.abs(freq - f)) for f in f0]
    except TypeError:
        return np.argmin(np.abs(freq - f0))


def __product_other_freqs(spec, indices, synthetic=(), t=None):
    p1 = np.prod(
        [
            amplitude * np.exp(2j * np.pi * freq * t + phase)
            for (freq, amplitude, phase) in synthetic
        ],
        axis=0,
    )
    p2 = np.prod(spec[:, indices[len(synthetic):]], axis=1)
    return p1 * p2


def functools_reduce(a):
    return functools.reduce(operator.concat, a)
