from __future__ import annotations

import numpy as np

from .constants import PROTON
from .types import MassError


def mz(mass: float, charge: int) -> float:
    return (mass + (charge * PROTON)) / charge


def get_tolerance(
    tolerance: float = 25.0,
    theoretical: float | None = None,
    unit: MassError = "ppm",
) -> float:
    """Calculates the toleranc in daltons from either a dalton tolerance or a ppm.

    tolerance.

    Returns
    -------
        float, the tolerance value in daltons

    Examples
    --------
        >>> get_tolerance(25.0, 2000.0, "ppm")
        0.05
        >>> get_tolerance(0.02, 2000.0, "da")
        0.02
        >>> get_tolerance(25.0, np.array([1000.0, 1500.0, 2000.0]), "da")
        25.0
        >>> get_tolerance(25.0, np.array([1000.0, 1500.0, 2000.0]), "ppm")
        array([0.025 , 0.0375, 0.05  ])

    Args
    ----
      tolerance: Tolerance value to be used (Default value = 25.0)
      theoretical: Theoretical m/z to be used (only used for ppm)
      unit: Lietrally da for daltons or ppm for ... ppm (Default value = "ppm")
    """
    if unit == "ppm":
        if theoretical is None:
            raise ValueError("Theoretical m/z must be provided for ppm")
        return theoretical * tolerance / 10**6
    elif unit == "da":
        return tolerance
    else:
        raise ValueError(f"unit {unit} not implemented")


def is_in_tolerance(
    theoretical: float,
    observed: float,
    tolerance: float = 25.0,
    unit: MassError = "ppm",
) -> bool:
    """Checks wether an observed mass is close enough to a theoretical mass.

    Returns
    -------
        bool, Wether the value observed is within the tolerance of the theoretical value

    Examples
    --------
        >>> is_in_tolerance(2000.0, 2000.0, 25.0, "ppm")
        True
        >>> is_in_tolerance(2000.0, 2000.0, 25.0, "da")
        True
        >>> is_in_tolerance(2000.0, 2000.4, 25.0, "ppm")
        False
        >>> obs = np.array([1000.0, 1500.0, 2000.0])
        >>> theo = np.array([1000.001, 1500.001, 2000.2])
        >>> is_in_tolerance(theo, obs, 25.0, "ppm")
        array([ True,  True, False])

    Args
    ----
      theoretical: Theoretical m/z
      observed: Observed m/z
      tolerance: Tolerance value to be used (Default value = 25.0)
      unit: Lietrally da for daltons or ppm for ... ppm (Default value = "ppm")
    """
    mz_tolerance = get_tolerance(
        theoretical=theoretical, tolerance=tolerance, unit=unit
    )
    lower = observed - mz_tolerance
    upper = observed + mz_tolerance

    return (lower <= theoretical) & (theoretical <= upper)


def find_matching_sorted(
    A, B, max_diff=0.5, in_range_fun=None
) -> list(tuple[int, int]):
    """Finds the matching between two sorted lists of floats.

    Args:
        A (List[float]): Sorted list of floats
        B (List[float]): Sorted list of floats
        max_diff (float, optional): Maximum allowed difference between
            elements in A and B. Defaults to 0.5.
        in_range_fun (Callable, optional): Function that takes two floats
            and returns True if they are in some definition of range.
            Defaults to None.

    Returns:
        List[Tuple[int, int], None, None]: Generator of tuples
    """

    if in_range_fun is None:

        def in_range_fun(x, y):
            return abs(x - y) <= max_diff

    elems = []
    min_ib = 0

    for ia, a in enumerate(A):
        min_val = a - max_diff
        for ib, b in enumerate(B[min_ib:], start=min_ib):
            if b < min_val:
                min_ib = ib
                continue
            elif in_range_fun(a, b):
                elems.append((ia, ib))

            if b > a + max_diff:
                break

    if len(elems) == 0:
        ia, ib = [], []
    else:
        ia, ib = zip(*elems)
    return np.array(ia, dtype=int), np.array(ib, dtype=int)


def sort_all(keys, *args):
    """Sorts all the arrays in args by ordered version of the array in keys.

    Examples
    --------
        >>> keys = np.array([1, 3, 2, 4])
        >>> foo = np.array([1, 2, 3, 4])
        >>> bar = np.array([5, 6, 7, 8])
        >>> keys, foo, bar = sort_all(keys, foo, bar)
        >>> foo
        array([1, 3, 2, 4])
        >>> bar
        array([5, 7, 6, 8])

    Args
    ----
        keys: Array to be used as the key for sorting
        *args: Arrays to be sorted
    """

    index = np.argsort(keys)
    out_args = [keys] + [x for x in args]
    out = [np.array(x)[index] for x in out_args]
    return out


def find_matching(A, B, max_diff=0.5, in_range_fun=None) -> tuple[np.array, np.array]:
    """Finds the matching between two lists of floats.

    Args:
        A (List[float]): List of floats
        B (List[float]): List of floats
        max_diff (float, optional): Maximum allowed difference between
            elements in A and B. Defaults to 0.5.
        in_range_fun (Callable, optional): Function that takes two floats
            and returns True if they are in some definition of range.
            Defaults to None.

    Returns:
        np.array, np.array
    """

    a_indices = np.array(range(len(A)), dtype=int)
    b_indices = np.array(range(len(B)), dtype=int)

    A, a_indices = sort_all(A, a_indices)
    B, b_indices = sort_all(B, b_indices)

    ia, ib = find_matching_sorted(A, B, max_diff, in_range_fun)

    return a_indices[ia], b_indices[ib]


def annotate_peaks(
    theo_mz: np.array,
    mz: np.array,
    tolerance: float = 25.0,
    unit: MassError = "ppm",
) -> tuple[np.ndarray, np.ndarray]:
    """Annotate_peaks Assigns m/z peaks to annotations.

    Arguments:
        theo_mz {np.array}: Theoretical m/z values
        mz {np.array}: Observed m/z values
        tolerance {float}: Tolerance value to be used (Default value = 25.0)
        unit {MassError}: Lietrally da for daltons or ppm for ...
            ppm (Default value = "ppm")

    Returns:
        np.array, np.array:
            The two arrays are the same length to each other.
            They contain [1] the indices in the theoretical m/z array.
            that match [2] the indices in the observed m/z array.

    Examples:
        >>> dumm1 = np.array(
        ...     [
        ...         1500.0,
        ...         2000.0,
        ...         1000.0,
        ...     ]
        ... )
        >>> dumm2 = np.array([1000.001, 1600.001, 2000.2])
        >>> annotate_peaks(dumm1, dumm2, 1, "da")
        (array([2, 1]), array([0, 2]))
        >>> (
        ...     dumm1[annotate_peaks(dumm1, dumm2, 1, "da")[1]],
        ...     dumm2[annotate_peaks(dumm1, dumm2, 1, "da")[0]],
        ... )
        (array([1500., 1000.]), array([2000.2  , 1600.001]))
        >>> theo_dumm1 = (np.array(range(20)) * 0.01) + 1000
        >>> obs_dumm2 = np.array([1000.001, 1600.001, 2000.2])
        >>> annotate_peaks(theo_dumm1, obs_dumm2, 1, "da")
        (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
           13, 14, 15, 16, 17, 18, 19]),
           array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        >>> theoretical_peaks = np.array([100.0, 200.0, 300.0, 500.0])
        >>> theoretical_labels = np.array(["a", "b", "c", "d"])
        >>> mzs = np.array([10, 100.0, 100.001, 150.0, 200.0, 300.0, 400.0])
        >>> ints = np.array([0.1, 1.0, 0.2, 5.0, 31.0, 2.0, 3.0])
        >>> x, y = annotate_peaks(theoretical_peaks, mzs)
        >>> x
        array([0, 0, 1, 2])
        >>> y
        array([1, 2, 4, 5])
        >>> theoretical_labels[x]
        array(['a', 'a', 'b', 'c'], dtype='<U1')
        >>> ints[y]
        array([ 1. ,  0.2, 31. ,  2. ])
    """
    max_delta = get_tolerance(tolerance=tolerance, theoretical=max(mz), unit=unit)

    def diff_fun(theo, obs):
        tol = get_tolerance(tolerance=tolerance, theoretical=theo, unit=unit)
        return abs(theo - obs) <= tol

    return find_matching(theo_mz, mz, max_delta, diff_fun)
