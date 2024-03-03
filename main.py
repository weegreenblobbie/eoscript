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
    minimum_time_step = 3.0
)

script.camera = "Nikon Z7"
script.fstop = 8

script.file_comment = "# C1 -> C2 partials"
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

script.phase = "C2"
script.offset = -15.0
script.iso = 64
script.exposure = _1 / 500
script.comment = "diamond ring / baily's beads"
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 1"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 2"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 3"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 4"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 5"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 6"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 7"
# script.capture_bracket(7)
# script.offset += 1
# script.file_comment = "# C2 diamond ring / baily's beads - bracket 8"
# script.capture_bracket(7)

script.comment = "bracket test"

script.exposure = _1 / 15
script.capture_bracket(19)




script.save("nick.csv")
