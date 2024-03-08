from eoscript import Exposure, Script

#------------------------------------------------------------------------------
# Write you scirpt!

_1 = Exposure(1)

script = Script(
    c1  = "2024/04/08 12:21:27.5 PM",
    c2  = "2024/04/08  1:38:46.6 PM",
    max = "2024/04/08  1:40:58.0 PM",
    c3  = "2024/04/08  1:43:09.4 PM",
    c4  = "2024/04/08  3:01:20.9 PM",
    minimum_time_step = 0.30,
)

script.camera = "Nikon Z7"
script.fstop = 8

script.file_comment = "#-----------------------------------------------------"
script.file_comment = "# C1 -> C2 partials"
script.file_comment = "#-----------------------------------------------------"
script.iso = 800
script.phase = "C1"
script.exposure = _1 / 400
script.comment = "C1 -> C2 partials"

script.capture("12:23:27 PM")
script.capture("12:31:35 PM")
script.capture("12:39:43 PM")
script.capture("12:47:51 PM")
script.capture("12:55:59 PM")
script.capture("01:04:07 PM")
script.capture("01:12:15 PM")
script.capture("01:20:23 PM")
script.capture("01:28:31 PM")
script.capture("01:36:46 PM")

script.file_comment = "#-----------------------------------------------------"
script.file_comment = "# C2 -> diamond ring & baily's beads"
script.file_comment = "#-----------------------------------------------------"

script.phase = "C2"
script.offset = -40.0
script.iso = 64
script.exposure = _1 / 500
script.comment = "diamond ring speed test"

#script.file_comment = "SETEXP,C2,-,00:00:33.0,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring speed test"

script.send_exposure()
script.offset += 3
script.release_command = "TAKEPIC"


# Speed test.
for _ in range(60):
    script.capture()

script.save("nick.csv")
