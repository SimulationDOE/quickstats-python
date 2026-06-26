#!/usr/bin/env python

import math

class QuickStats:
    """
    Computationally stable and efficient basic descriptive statistics.
    This class uses Kalman Filter updating to tally sample mean and sum
    of squares, along with min, max, and sample size. Sample variance,
    standard deviation and standard error are calculated on demand.
    """

    def __init__(self):
        """Initialize state vars in a new QuickStats object using reset()."""
        self.reset()

    def reset(self):
        """
        Reset all state vars to initial values.

          ssd = n = 0
          sample_mean = sample_variance = NaN
          min = infinity
          max = -infinity

        Returns:
            self (QuickStats) - to facilitate method chaining
        """
        self.__ssd = 0.0
        self.__n = 0
        self.__sample_mean = math.nan
        self.__max = -math.inf
        self.__min = math.inf
        return self

    def new_obs(self, datum):
        """
        Update the sample size, sample mean, sum of squares, min, and max given
        a new observation. All but the sample size are maintained as floating point.

        Parameters:
            datum (numeric) : the new observation
        Returns:
            self (QuickStats) - to facilitate method chaining
        Raises:
            RuntimeError if datum is non-numeric
        """
        x = float(datum)
        if x > self.__max:
            self.__max = x
        if x < self.__min:
            self.__min = x
        if self.__n > 0:
            delta = x - self.__sample_mean
            self.__n += 1
            self.__sample_mean += delta / self.__n
            self.__ssd += delta * (x - self.__sample_mean)
        else:
            self.__sample_mean = x
            self.__n = 1
        return self

    def add_all(self, iterable_collection):
        """
        Update the statistics with all elements of an enumerable set.

        Parameters:
            iterable_collection (Iterable[numeric]) : a collection of new observations.
        Returns:
            self (QuickStats) - to facilitate method chaining
        """
        for x in iterable_collection:
            self.new_obs(x)
        return self

    add_list = add_all
    add_set = add_all

    @property
    def sample_variance(self):
        """
        Calculates the unbiased sample variance on demand (divisor is n-1).

        Returns:
            sample variance (float) of the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return (self.__ssd / (self.__n - 1)) if self.__n > 1 else math.nan

    var = sample_variance

    @property
    def mle_sample_variance(self):
        """
        Calculates the MLE sample variance on demand (divisor is n).

        Returns:
            MLE sample variance (float) of the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return (self.__ssd / self.__n) if self.__n > 1 else math.nan

    mle_var = mle_sample_variance

    @property
    def standard_deviation(self):
        """
        Calculates the square root of the unbiased sample variance on demand.

        Returns:
            sample standard deviation (float) of the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return math.sqrt(self.sample_variance) if self.n > 1 else math.nan

    s = standard_deviation
    std_dev = standard_deviation

    @property
    def mle_standard_deviation(self):
        """
        Calculates the square root of the MLE sample variance on demand.

        Returns:
            MLE standard deviation (float) of the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return math.sqrt(self.mle_sample_variance) if self.n > 1 else math.nan

    mle_s = mle_standard_deviation
    mle_std_dev = mle_standard_deviation

    @property
    def standard_error(self):
        """
        Calculates sqrt(sample_variance / n) on demand.

        Returns:
            unbiased sample standard error (float) of the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return math.sqrt(self.sample_variance / self.__n) if self.n > 1 else math.nan

    std_err = standard_error

    @property
    def mle_standard_error(self):
        """
        Calculates sqrt(mle_sample_variance / n) on demand.

        Returns:
            sample standard error (float) of the data based on MLE,
            or NaN if this is a new or just-reset QuickStats object.
        """
        return math.sqrt(self.mle_sample_variance / self.__n) if self.n > 1 else math.nan

    mle_std_err = mle_standard_error

    def loss(self, *, target=0.0):
        """
        Estimates quadratic loss (a la Taguchi) relative to a specified
        target value.

        Parameters:
            target (float) : the designated target value for the loss function.
        Returns:
            quadratic loss (float) calculated for the data, or NaN if this is a
            new or just-reset QuickStats object.
        """
        return (
            math.nan
            if self.n < 2
            else (self.avg - target) ** 2 + self.var
        )

    # getters for n, sample_mean, min, max, ssd

    @property
    def n(self):
        """current sample size"""
        return self.__n

    @property
    def sample_mean(self):
        """current average of the data"""
        return self.__sample_mean

    @property
    def min(self):
        """current minimum of the data"""
        return self.__min

    @property
    def max(self):
        """current maximum of the data"""
        return self.__max

    @property
    def ssd(self):
        """current sum of squared deviations from the avergage of the data"""
        return self.__ssd

    average = sample_mean
    avg = sample_mean
    sample_size = n
    sum_squared_deviations = ssd
