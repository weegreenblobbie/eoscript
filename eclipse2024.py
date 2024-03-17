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
    script.release_command = "TAKEPIC"
    script.iso = 800
    script.exposure = _1 / 400
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"

def _capture_partial(phase0, phase1, offset, num_exposures):
    script.offset = offset
    comment = f"{phase0} -> {phase1} partial at {offset}"
    for i in range(num_exposures):
        script.comment = comment + f" {i + 1}/{num_exposures}"
        script.capture()
    script.file_comment = ""

#------------------------------------------------------------------------------
# C1 partials

NUM_PHOTOS_PER_PARTIAL = 8

_setup_for_partials("C1", "C2")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!

_capture_partial("C1", "C2", "17:23:27", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "17:31:35", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "17:39:43", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "17:47:51", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "17:55:59", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "18:04:07", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "18:12:15", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "18:20:23", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "18:28:31", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C1", "C2", "18:36:46", NUM_PHOTOS_PER_PARTIAL)

#------------------------------------------------------------------------------
# C2 diamond ring

def _diamond_ring(phase, offset):
    script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
    script.phase = phase
    script.offset = offset
    script.iso = 100
    script.exposure = _1 / 500
    script.min_time_step = MIN_STEP_FAST
    script.comment = f"fast burst {script.exposure}s f/{script.fstop} iso {script.iso}"
    script.offset += MIN_STEP_FAST  # A litte more margin.
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    for _ in range(40):
        script.capture()

_diamond_ring("C2", -11.4 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# Fast, manual stacks for ultimate post processing.

def _fast_manual_stacks(label, reverse=False, skip_first_setexp=False):
    script.banner(f"{label}: fast bursts for stacking")
    script.min_time_step = MIN_STEP_FAST
    script.iso = 800
    NUM_PHOTOS_PER_STACK = 9
    exp = 1.0 / 500
    exposures = [exp * (2**i) for i in range(12)]
    if reverse:
        exposures = exposures[::-1]
    for i, exposure in enumerate(exposures):
        script.exposure = exposure
        script.comment = script.comment = f"fast burst {script.exposure}s f/{script.fstop} iso {script.iso}"
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

#------------------------------------------------------------------------------
# C3 diamond ring

_diamond_ring("C3", -2.0 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# C3 partials

_setup_for_partials("C3", "C4")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!

_capture_partial("C3", "C4", "18:45:09", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "18:53:23", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:01:37", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:09:51", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:18:05", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:26:19", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:34:33", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:42:47", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:51:01", NUM_PHOTOS_PER_PARTIAL)
_capture_partial("C3", "C4", "19:59:20", NUM_PHOTOS_PER_PARTIAL)

script.save("eclipse2024.csv")
