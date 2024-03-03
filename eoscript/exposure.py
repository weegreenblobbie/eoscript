from bisect import bisect_left
from fractions import Fraction
import copy
import math

# Due do weird rounding, use a lookup table in 1/3 EV steps.
_COMMON_EXPOSURES = [
    (1, 8000),
    (1, 6400),
    (1, 5000),
    (1, 4000),
    (1, 3200),
    (1, 2500),
    (1, 2000),
    (1, 1600),
    (1, 1250),
    (1, 1000),
    (1, 800),
    (1, 640),
    (1, 500),
    (1, 400),
    (1, 320),
    (1, 250),
    (1, 200),
    (1, 160),
    (1, 125),
    (1, 100),
    (1, 80),
    (1, 60),
    (1, 50),
    (1, 40),
    (1, 30),
    (1, 25),
    (1, 20),
    (1, 15),
    (1, 13),
    (1, 10),
    (1, 8),
    (1, 6),
    (1, 5),
    (1, 4),
    (1, 3),
    (1, 2.5),
    (1, 2),
    (1, 1.6),
    (1, 1.3),
    (1, 1),
    (1.3, 1),
    (1.6, 1),
    (2, 1),
    (2.5, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (8, 1),
    (10, 1),
    (13, 1),
    (15, 1),
    (20, 1),
    (25, 1),
    (30, 1),
]

_LUT_TIMES = [float(x[0])/float(x[1]) for x in _COMMON_EXPOSURES]


def lookup_exposure(time):
    """
    Given the time, finds the nearest exposure and returns a fration as a
    tuple.
    """
    if time < _LUT_TIMES[0]: return _COMMON_EXPOSURES[0]
    if time > _LUT_TIMES[-1]: return _COMMON_EXPOSURES[-1]
    idx1 = bisect_left(_LUT_TIMES, time)
    idx0 = idx1 - 1
    dist0 = abs(time - _LUT_TIMES[idx0])
    dist1 = abs(time - _LUT_TIMES[idx1])
    if dist0 < dist1:
        return _COMMON_EXPOSURES[idx0]
    return _COMMON_EXPOSURES[idx1]


class Exposure:

    def __init__(self, numerator, denominator=1):
        assert numerator > 0, f"numerator must be > 0, got {numerator}"
        assert denominator > 0, f"denominator must be > 0, got {denominator}"
        self._time = float(numerator) / float(denominator)

    def __gt__(self, other):
        if isinstance(other, float):
            return self._time > other
        assert isinstance(other, Exposure)
        return self._time > other._time

    def __truediv__(self, denominator):
        assert denominator != 0, "Division by 0!"
        return Exposure(self._time, denominator)

    def __float__(self):
        return self._time

    def __add__(self, ev_stops):
        """
        Manipulate exposure via exposure values, i.e. stops of light.

        See https://en.wikipedia.org/wiki/Exposure_value
        """
        out = copy.copy(self)
        # Convert to exposure value.
        ev = math.log2(1.0 / self._time)
        # Add stops.
        ev -= ev_stops
        # Convert back to time.
        time = 1.0 / 2**ev
        out = Exposure(1)
        out._time = time
        #return Exposure(time)
        return out

    def __sub__(self, ev_stops):
        return self.__add__(-ev_stops)

    def _normalize(self):
        n, d = lookup_exposure(self._time)
        self._time = float(n) / d

    def __str__(self):
        n, d = lookup_exposure(self._time)

        out = f"{n}"
        if d != 1:
            out += f"/{d}"
        return f"{out}"
