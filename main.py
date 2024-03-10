from eoscript import Exposure, Script

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script = Script(
    #                 UTC                Texas Local
    c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
    c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
    max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
    c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
    c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
    min_time_step = 0.30,
)

script.banner("C1 -> C2: partials")
script.phase = "C1"
script.camera = "Nikon Z7"
script.fstop = 8
script.iso = 800
script.exposure = Exposure(1) / 400
script.comment = "C1 -> C2 partials"

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script.capture("17:23:27")
script.capture("17:31:35")
script.capture("17:39:43")
script.capture("17:47:51")
script.capture("17:55:59")
script.capture("18:04:07")
script.capture("18:12:15")
script.capture("18:20:23")
script.capture("18:28:31")
script.capture("18:36:46")

script.save("eclipse2024.csv")
