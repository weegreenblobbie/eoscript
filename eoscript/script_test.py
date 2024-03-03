import unittest
import textwrap

from eoscript import Script, Exposure

def compare(actual, expected, debug=False):
    passes = actual == expected
    if debug and not passes:
        with open("actual.txt", "w") as fout:
            fout.write(actual)
        with open("expected.txt", "w") as fout:
            fout.write(expected)
        print("Wrote actual.txt and expected.txt")
    return passes

class TestExposure(unittest.TestCase):

    def test_basics(self):
        script = Script()
        script.comment = "test basics"
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 800
        script.exposure = Exposure(1) / 400
        script.phase = "C1"
        script.capture()
        script.capture()
        script.capture()
        script.file_comment = "# testing a file comment"
        script.capture()
        script.capture()
        script.capture()

        expected = textwrap.dedent("""\
            #Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
            TAKEPIC,C1,+,00:00:00.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:03.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:06.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            # testing a file comment
            TAKEPIC,C1,+,00:00:09.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:12.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:15.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            """)
        assert compare(str(script), expected)

    def test_bracket(self):
        script = Script()
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 800
        script.exposure = Exposure(1) / 400
        script.offset = -15.0
        script.phase = "C2"
        script.comment = "test bracket"
        script.capture_bracket(3)
        script.file_comment = "# testing a file comment"
        script.capture_bracket(5)
        expected = textwrap.dedent("""\
            #Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
            TAKEPIC,C2,-,00:00:15.0,Nikon Z7,1/800 , 8.0, 800,0.0,RAW+F-JPG,None,N,test bracket
            TAKEPIC,C2,-,00:00:12.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            TAKEPIC,C2,-,00:00:09.0,Nikon Z7,1/200 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            # testing a file comment
            TAKEPIC,C2,-,00:00:06.0,Nikon Z7,1/1600, 8.0, 800,0.0,RAW+F-JPG,None,N,test bracket
            TAKEPIC,C2,-,00:00:03.0,Nikon Z7,1/800 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            TAKEPIC,C2,+,00:00:00.0,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            TAKEPIC,C2,+,00:00:03.0,Nikon Z7,1/200 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            TAKEPIC,C2,+,00:00:06.0,Nikon Z7,1/100 , 8.0, 800,0.0,RAW+F-JPG,None,Y,test bracket
            """)
        assert compare(str(script), expected)

    def test_long_exposure(self):
        script = Script()
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 64
        script.exposure = Exposure(8)
        script.offset = 0.0
        script.phase = "MAX"
        script.comment = "long exposure"
        script.capture()
        script.capture()
        script.capture()
        expected = textwrap.dedent("""\
            #Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
            TAKEPIC,MAX,+,00:00:00.0,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            TAKEPIC,MAX,+,00:00:11.0,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            TAKEPIC,MAX,+,00:00:22.0,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            """)
        assert compare(str(script), expected)
