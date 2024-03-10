from eoscript import Exposure, Script

# Ultimate Eclipse capture for 4m20s of totality.

MIN_STEP_FAST = 0.333 # Verify your setup to see how fast you can go!
MIN_STEP_SLOW = 1.250 # Verify your setup with USB updates.

_1 = Exposure(1)

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script = Script(
    #                 UTC                LOCAL TEXAS
    c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
    c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
    max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
    c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
    c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
)

script.camera = "Nikon Z7"
script.fstop = 8

def _setup_for_partials(phase0, phase1):
    script.banner(f"{phase0} -> {phase1}: partials")
    script.phase = phase0
    script.comment = f"{phase0} -> {phase1} partials"
    script.release_command = "TAKEPIC"
    script.iso = 64
    script.exposure = _1 / 25
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"

#------------------------------------------------------------------------------
# C1 partials

_setup_for_partials("C1", "C2")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script.capture("17:23:27")
script.capture()
script.capture()
script.capture("17:31:35")
script.capture()
script.capture()
script.capture("17:39:43")
script.capture()
script.capture()
script.capture("17:47:51")
script.capture()
script.capture()
script.capture("17:55:59")
script.capture()
script.capture()
script.capture("18:04:07")
script.capture()
script.capture()
script.capture("18:12:15")
script.capture()
script.capture()
script.capture("18:20:23")
script.capture()
script.capture()
script.capture("18:28:31")
script.capture()
script.capture()
script.capture("18:36:46")
script.capture()
script.capture()

#------------------------------------------------------------------------------
# C2 diamond ring

def _diamond_ring(phase, offset):
    script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
    script.phase = phase
    script.offset = offset
    script.iso = 64
    script.exposure = _1 / 500
    script.min_time_step = MIN_STEP_FAST
    script.comment = "fast burst"
    script.offset += MIN_STEP_FAST  # A litte more margin.
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    for _ in range(40):
        script.capture()

_diamond_ring("C2", -11.4 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# C2 long exposures

def _earthshine(label, exposure):
    script.banner(f"{label} long exposures for Earthshine")
    script.comment = "long exposures for Earthshine"
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"
    script.release_command = "TAKEPIC"
    script.iso = 64
    script.offset += MIN_STEP_FAST # A litte more margin.
    script.exposure = exposure
    script.capture()

_earthshine("C2", 20.0)

#------------------------------------------------------------------------------
# Fast, manual stacks for ultimate post processing.

def _fast_manual_stacks(label, reverse=False, skip_first_setexp=False):
    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.iso = 64
    NUM_PHOTOS_PER_STACK = 7
    exp = 1.0 / 1000
    exposures = [exp * (2**i) for i in range(13)]
    if reverse:
        exposures = exposures[::-1]
    for i, exposure in enumerate(exposures):
        script.exposure = exposure
        if i == 0 and skip_first_setexp:
            script.release_command = "RELEASE"
        else:
            script.offset += MIN_STEP_FAST # A little more margin
            script.send_exposure()
            script.offset += MIN_STEP_SLOW
        for _ in range(NUM_PHOTOS_PER_STACK):
            script.capture()

_fast_manual_stacks("C2 -> MAX", reverse=True)
script.file_comment = "C2,+,00:02:11  is Max Totality !!!"
_fast_manual_stacks("MAX -> C3", reverse=False, skip_first_setexp=True)

script.file_comment = "C2,+,00:04:22 is end of totality"

_earthshine("C2", 15.0)

#------------------------------------------------------------------------------
# C3 diamond ring

_diamond_ring("C3", -2.0 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# C3 partials

_setup_for_partials("C3", "C4")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script.capture("18:45:09")
script.capture()
script.capture()
script.capture("18:53:23")
script.capture()
script.capture()
script.capture("19:01:37")
script.capture()
script.capture()
script.capture("19:09:51")
script.capture()
script.capture()
script.capture("19:18:05")
script.capture()
script.capture()
script.capture("19:26:19")
script.capture()
script.capture()
script.capture("19:34:33")
script.capture()
script.capture()
script.capture("19:42:47")
script.capture()
script.capture()
script.capture("19:51:01")
script.capture()
script.capture()
script.capture("19:59:20")
script.capture()
script.capture()

script.save("eclipse2024.csv")
