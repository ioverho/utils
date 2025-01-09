from dataclasses import dataclass

import numpy as np
import scipy
import scipy.stats
import jaxtyping as jtyping


@dataclass(frozen=True)
class ProportionCIResult:
    p: float
    ub: float
    lb: float


def agresti_coull_interval(
    num_successes: int, num_trials: int, confidence_level: float = 0.95
) -> ProportionCIResult:
    """Generates an Agresti-Coull Binomial Confidence Interval.

    Note that the proportion value will be slightly shifted from the true (MLE) proportion.

    Args:
        num_successes (int): the number of trial successes
        num_trials (int): the total number of trials, e.g., success + failures
        confidence_level (float, optional): the confidence level to use. Must be between 0.0 and 1.0, exclusive. Defaults to 0.95.

    Returns:
        ProportionCIResult: the confidence interval, wrapped in a utility class
    """

    alpha = 1 - confidence_level

    z: jtyping.Float[np.typing.NDArray, "1"] = scipy.stats.norm.ppf(q=1 - alpha / 2)
    z2 = np.power(z, 2)

    n_adj = num_trials + z2

    p_adj = (num_successes + z2 / 2) / n_adj

    ub = p_adj + z * np.sqrt(p_adj * (1 - p_adj) / n_adj)
    lb = p_adj - z * np.sqrt(p_adj * (1 - p_adj) / n_adj)

    result = ProportionCIResult(p=float(p_adj), ub=float(ub), lb=float(lb))

    return result
