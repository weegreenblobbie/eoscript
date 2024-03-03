import unittest
from eoscript import Exposure

class TestExposure(unittest.TestCase):

    def test_basics(self):

        ex = Exposure(1)
        assert str(ex) == "1"

        ex = Exposure(1, 400)
        assert str(ex) == "1/400"

        ex = Exposure(1) / 500
        assert str(ex) == "1/500"

        ex = Exposure(4)
        assert str(ex) == "4"

        ex = Exposure(8/2)
        assert str(ex) == "4"

        _1 = Exposure(1)
        assert str(_1/400) == "1/400"
        assert str(_1/500) == "1/500"
        assert str(_1/800) == "1/800"


    def test_add_full_stops(self):

        ex = Exposure(1) / 8000
        assert str(ex) == "1/8000"
        ex += 1
        assert str(ex) == "1/4000"
        ex += 1
        assert str(ex) == "1/2000"
        ex += 1
        assert str(ex) == "1/1000"
        ex += 1
        assert str(ex) == "1/500"
        ex += 1
        assert str(ex) == "1/250"
        ex += 1
        assert str(ex) == "1/125"
        ex += 1
        assert str(ex) == "1/60"
        ex += 1
        assert str(ex) == "1/30"
        ex += 1
        assert str(ex) == "1/15"
        ex += 1
        assert str(ex) == "1/8"
        ex += 1
        assert str(ex) == "1/4"
        ex += 1
        assert str(ex) == "1/2"
        ex += 1
        assert str(ex) == "1"
        ex += 1
        assert str(ex) == "2"
        ex += 1
        assert str(ex) == "4"
        ex += 1
        assert str(ex) == "8"
        ex += 1
        assert str(ex) == "15"
        ex += 1
        assert str(ex) == "30"
        ex -= 1
        assert str(ex) == "15"
        ex -= 1
        assert str(ex) == "8"

    def test_add_third_stops(self):

        ex = Exposure(1) / 8000
        assert str(ex) == "1/8000"
        ex += 1/3.0
        assert str(ex) == "1/6400"
        ex += 1/3.0
        assert str(ex) == "1/5000"
        ex += 1/3.0
        assert str(ex) == "1/4000"
        ex += 1/3.0
        assert str(ex) == "1/3200"
        ex += 1/3.0
        assert str(ex) == "1/2500"
        ex += 1/3.0
        assert str(ex) == "1/2000"
        ex += 1/3.0
        assert str(ex) == "1/1600"
        ex += 1/3.0
        assert str(ex) == "1/1250"
        ex += 1/3.0
        assert str(ex) == "1/1000"
        ex += 1/3.0
        assert str(ex) == "1/800"
        ex += 1/3.0
        assert str(ex) == "1/640"
        ex += 1/3.0
        assert str(ex) == "1/500"
        ex += 1/3.0
        assert str(ex) == "1/400"
        ex += 1/3.0
        assert str(ex) == "1/320"
        ex += 1/3.0
        assert str(ex) == "1/250"
        ex += 1/3.0
        assert str(ex) == "1/200"
        ex += 1/3.0
        assert str(ex) == "1/160"
        ex += 1/3.0
        assert str(ex) == "1/125"
        ex += 1/3.0
        assert str(ex) == "1/100"
        ex += 1/3.0
        assert str(ex) == "1/80"
        ex += 1/3.0
        assert str(ex) == "1/60"
        ex += 1/3.0
        assert str(ex) == "1/50"
        ex += 1/3.0
        assert str(ex) == "1/40"
        ex += 1/3.0
        assert str(ex) == "1/30"
        ex += 1/3.0
        assert str(ex) == "1/25"
        ex += 1/3.0
        assert str(ex) == "1/20"
        ex += 1/3.0
        assert str(ex) == "1/15"
        ex += 1/3.0
        assert str(ex) == "1/13"
        ex += 1/3.0
        assert str(ex) == "1/10"
        ex += 1/3.0
        assert str(ex) == "1/8"
        ex += 1/3.0
        assert str(ex) == "1/6"
        ex += 1/3.0
        assert str(ex) == "1/5"
        ex += 1/3.0
        assert str(ex) == "1/4"
        ex += 1/3.0
        assert str(ex) == "1/3"
        ex += 1/3.0
        assert str(ex) == "1/2.5"
        ex += 1/3.0
        assert str(ex) == "1/2"
        ex += 1/3.0
        assert str(ex) == "1/1.6"
        ex += 1/3.0
        assert str(ex) == "1/1.3"
        ex += 1/3.0
        assert str(ex) == "1"
        ex += 1/3.0
        assert str(ex) == "1.3"
        ex += 1/3.0
        assert str(ex) == "1.6"
        ex += 1/3.0
        assert str(ex) == "2"
        ex += 1/3.0
        assert str(ex) == "2.5"
        ex += 1/3.0
        assert str(ex) == "3"
        ex += 1/3.0
        assert str(ex) == "4"
        ex += 1/3.0
        assert str(ex) == "5"
        ex += 1/3.0
        assert str(ex) == "6"
        ex += 1/3.0
        assert str(ex) == "8"
        ex += 1/3.0
        assert str(ex) == "10"
        ex += 1/3.0
        assert str(ex) == "13"
        ex += 1/3.0
        assert str(ex) == "15"
        ex += 1/3.0
        assert str(ex) == "20"
        ex += 1/3.0
        assert str(ex) == "25"
        ex += 1/3.0
        assert str(ex) == "30"

