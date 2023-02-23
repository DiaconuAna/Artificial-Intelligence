# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""

# θ(theta) corresponds to the angular position (positive is clockwise) of the pendulum
# θ will be x1 and we assume −40° <= x1 <= 40°
THETA = {
    'NVB': (None, -25, -40),
    'NB': (-40, -10),
    'N': (-20, 0),
    'Z': (-5, 5),
    'P': (0, 20),
    'PB': (10, 40),
    'PVB': (25, None, 40)  # should be 50 ?
}

# ω(omega) corresponds to the angular speed
# ω will be x2 and we assume −8 °/s <= x2 <= 8 °/s
# Angular speed is the measure of how fast the central angle of a rotating body changes with respect to time.

OMEGA = {
    'NB': (None, -3, -8),
    'N': (-6, 0),
    'Z': (-1, 1),
    'P': (0, 6),
    'PB': (3, None, 8)
}

# To partition the control space as output, we construct nine membership functions for u on its universe which is
# −32 N <= u <= 32 N
vectors = {
    'NVVB': -32,
    'NVB': -24,
    'NB': -16,
    'N': -8,
    'Z': 0,
    'P': 8,
    'PB': 16,
    'PVB': 24,
    'PVVB': 32,
}

# (PVB) -positive very big
# (PB) - positive big
# (P) - positive
# (Z) - zero
# (N) - negative
# (NB)  - negative big
# (NVB)  negative very big

#     PB      P       Z       N       NB    (x2)
# PVB PVVB    PVVB    PVB     PB      P
# PB  PVVB    PVB     PB      P       Z
# P   PVB     PB      P       Z       N
# Z   PB      P       Z       N       NB
# N   P       Z       N       NB      NVB
# NB  Z       N       NB      NVB     NVVB
# NVB N       NB      NVB     NVVB    NVVB
# (x1)
# example:
# if (x1 = PVB) and (x2 = PB) THEN u = PVVB
# if (x1 - PVB) and (x2 = P) THEN u = PVVB

# rules for the fuzzy system
fuzzyRules = {
    'PVB': {
        'PB': 'PVVB',
        'P': 'PVVB',
        'Z': 'PVB',
        'N': 'PB',
        'NB': 'P'},
    'PB': {
        'PB': 'PVVB',
        'P': 'PVB',
        'Z': 'PB',
        'N': 'P',
        'NB': 'Z'},
    'P': {
        'PB': 'PVB',
        'P': 'PB',
        'Z': 'P',
        'N': 'Z',
        'NB': 'N'},
    'Z': {
        'PB': 'PB',
        'P': 'P',
        'Z': 'Z',
        'N': 'N',
        'NB': 'NB'},
    'N': {
        'NB': 'NVB',
        'N': 'NB',
        'Z': 'N',
        'P': 'Z',
        'PB': 'P'},
    'NB': {
        'PB': 'Z',
        'P': 'N',
        'Z': 'NB',
        'N': 'NVB',
        'NB': 'NVVB'},
    'NVB': {
        'PB': 'N',
        'P': 'NB',
        'Z': 'NVB',
        'N': 'NVVB',
        'NB': 'NVVB'},
}


class Fuzzifier:
    """
    Here we compute the membership degrees for Theta and Omega to each set using the data
    from above and the triangle formula from the lecture
    """

    def __init__(self, start, end, mean=None):
        self.__start = start
        self.__end = end
        self.__mean = mean
        if self.__mean is None:
            self.computeMean()

    def computeMean(self):
        self.__mean = (self.__start + self.__end) / 2

    def membershipDegree(self, x):
        """
        Compute the membership degree using the triangle formula
        Returns
        -------

        """
        if self.__start is not None and self.__start <= x < self.__mean:
            return (x - self.__start) / (self.__mean - self.__start)
        elif self.__end is not None and self.__mean <= x < self.__end:
            return (self.__end - x) / (self.__end - self.__mean)
        else:
            return 0


# gives a fuzzy membership function to a given range
def fuzzify(ranges):
    return {
        fuzzySet: Fuzzifier(*interval)
        for (fuzzySet, interval) in ranges.items()}


# computes the membership for each fuzzy set based on its associated function (values between 0 and 1)
def computeMembership(value, inputFunctions):
    return {
        fuzzySet: function.membershipDegree(value)
        for (fuzzySet, function) in inputFunctions.items()}


thetaFunctions = fuzzify(THETA)
omegaFunctions = fuzzify(OMEGA)


def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or

    None :if we have a division by zero

    """
    # compute the membership degree for input params
    tMembershipValue = computeMembership(t, thetaFunctions)
    wMembershipValue = computeMembership(w, omegaFunctions)

    # membership degree of F for each set
    FdegreeTable = {}

    for thetaSet in fuzzyRules:
        for omegaSet, f in fuzzyRules[thetaSet].items():
            # in each cell of the rules table take the minimum
            # of the membership values of the index set
            value = min(tMembershipValue[thetaSet], wMembershipValue[omegaSet])

            # the membership degree of F to each class will be the macmimum value
            # for that class taken from the rules' table
            if f not in FdegreeTable:
                FdegreeTable[f] = value
            else:
                FdegreeTable[f] = max(value, FdegreeTable[f])

        # defuzzify the results for F using a weighted average of the
        # membership degrees and the b values of the sets

    sumOfForces = 0
    product = 0

    for force in FdegreeTable.keys():
        sumOfForces += FdegreeTable[force]
        product += FdegreeTable[force] * vectors[force]

    if sumOfForces != 0:
        finalForce = product / sumOfForces
    else:
        finalForce = 0

    return finalForce





