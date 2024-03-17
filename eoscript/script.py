import copy
import datetime
import dateutil.parser

from .exposure import Exposure


class Quality:
    raw = "RAW"           # RAW only
    raw_fjpg = "RAW+F-JPG"  # RAW + Fine JPEG

class Dur:
    """Duration"""
    minute = 60.0
    hour = 60 * minute


def hours_minuts_seconds(total_seconds):
    if isinstance(total_seconds, datetime.timedelta):
        total_seconds = total_seconds.total_seconds()
    total_seconds = abs(total_seconds)
    hours = int(total_seconds / Dur.hour)
    total_seconds -= Dur.hour * hours
    minutes = int(total_seconds / Dur.minute)
    seconds = total_seconds - Dur.minute * minutes
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


class Script:
    def __init__(self, c1=None, c2=None, max=None, c3=None, c4=None, min_time_step=3.0):
        self._min_time_step = min_time_step
        self._camera = None
        self._comment = ""
        self._events = []
        self._exposure = None
        self._fstop = None
        self._iso = None
        self._release_command = "TAKEPIC"
        self._phase = None
        self._offset = 0.0
        self._qualiy = Quality.raw_fjpg
        self._mirror_lock_up = 0.0  # Mirrorless cameras don't have a mirror!
        self._incremental = 'N' # Only changes in camera settings and transmitted via USB.
        self._phase_to_time = None
        self._c1 = dateutil.parser.parse(c1) if c1 else c1
        self._c2 = dateutil.parser.parse(c2) if c2 else c2
        self._max = dateutil.parser.parse(max) if max else max
        self._c3 = dateutil.parser.parse(c3) if c3 else c3
        self._c4 = dateutil.parser.parse(c4) if c4 else c4
        self._release_duration = 0.050
        if any([c1, c2, max, c3, c4]):
            assert all([c1, c2, max, c3, c4]), f"If any phase is initialized, they all must be initialized"
            assert self._c1 < self._c2
            assert self._c2 < self._max
            assert self._max < self._c3
            assert self._c3 < self._c4
            self._phase_to_time = {"C1": self._c1, "C2": self._c2, "MAX": self._max, "C3": self._c3, "C4": self._c4}

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value.replace(",", "")

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        self.release_command = "TAKEPIC"
        if isinstance(value, float):
            self._exposure = Exposure(value)
        else:
            self._exposure = value

    @property
    def file_comment(self):
        return None

    @file_comment.setter
    def file_comment(self, comment):
        if not comment.startswith("#"):
            self._events.append(f"# {comment}")
        else:
            self._events.append(comment)

    @property
    def fstop(self):
        return self._fstop

    @fstop.setter
    def fstop(self, value):
        self.release_command = "TAKEPIC"
        self._fstop = value

    @property
    def incremental(self):
        return self._incremental

    @incremental.setter
    def incremental(self, value):
        assert value in {"Y", "N"}
        self._incremental = value

    @property
    def iso(self):
        return self._iso

    @iso.setter
    def iso(self, value):
        self.release_command = "TAKEPIC"
        self._iso = value

    @property
    def min_time_step(self):
        return self._min_time_step

    @min_time_step.setter
    def min_time_step(self, value):
        self._min_time_step = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        if isinstance(value, str):
            assert self._phase_to_time, 'To use HH:MM:SS times, please pass phase times to, i.e. Script(c1 = "YYYY/MM/DD HH:MM:SS.f", ...)'
            phase = self._phase_to_time[self._phase]
            time = dateutil.parser.parse(f"{phase.year}/{phase.month}/{phase.day} {value}")
            self._offset = (time - phase).total_seconds()
        else:
            self._offset = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        assert value in {"C1", "C2", "MAX", "C3", "C4"}
        self._phase = value
        self._offset = 0

    @property
    def release_command(self):
        return self._release_command

    @release_command.setter
    def release_command(self, command):
        assert command in {"TAKEPIC", "RELEASE"}
        self._release_command = command

    def banner(self, message, width=120):
        self.file_comment = f"#{width * '-'}"
        self.file_comment = f"# {message}"
        self.file_comment = f"#{width * '-'}"

    def capture(self, exposure=None):
        # A phase must have been selected.
        assert self._phase, "Phase hasn't been specified!"
        assert self._camera, "Camera hasn't been specified!"
        assert self._fstop, "F-Stop hasn't been specified!"
        assert self._iso, "ISO hasn't been specified!"

        if exposure is not None:
            self.release_command = "TAKEPIC"
        exposure = copy.copy(exposure) if exposure else copy.copy(self._exposure)
        assert type(exposure) in {int, float, Exposure}, f"Expected exposure type to be in [int, float, Exposure], got {type(exposure)}"
        if type(exposure) in {int, float}:
            exposure = Exposure(exposure)

        if self._release_command == "RELEASE":
            self._events.append([
                "RELEASE",
                self._offset,
                self._phase,
                self._camera,
                f"{self._release_duration:6.3f}",
                "",
                "",
                "",
                "",
                self._comment,
            ])

        else:
            self._events.append([
                self._release_command,
                self._offset,
                self._phase,
                self._camera,
                exposure,
                self._fstop,
                self._iso,
                self._mirror_lock_up,
                self._incremental,
                self._comment,
            ])

        self.offset += float(exposure) + self._min_time_step

    def send_exposure(self, release_duration=0.050):
        # A phase must have been selected.
        assert self._phase, "Phase hasn't been specified!"
        assert self._camera, "Camera hasn't been specified!"
        assert self._fstop, "F-Stop hasn't been specified!"
        assert self._iso, "ISO hasn't been specified!"
        exposure = copy.copy(self._exposure)
        self._events.append([
            "SETEXP",
            self._offset,
            self._phase,
            self._camera,
            exposure,
            self._fstop,
            self._iso,
            self._mirror_lock_up,
            "N",
            "sending all camera exposure settings via USB",
        ])
        self._incremental = "Y"
        self.release_command = "RELEASE"
        self._release_duration = release_duration


    def capture_bracket(self, num_exposures, ev_step=1):
        """
        Catpures a set of bracketed shots centerered on the current exposure
        setting.
        """
        assert num_exposures % 2 == 1, f"num_exposures must be odd, got {num_exposures}"
        assert num_exposures >= 3, f"num_exposures must be >= 3, got {num_exposures}"

        center = self._exposure
        running_ev_stops = 0
        exposures = [(center, running_ev_stops)]

        # How many faster or slower are left?
        num_exposures -= 1
        num_exposures //= 2
        # Faster exposures.
        exposure = copy.copy(center)
        for i in range(num_exposures):
            exposure -= ev_step
            running_ev_stops -= ev_step
            exposures.append((exposure, running_ev_stops))

        # Slower exposures.
        running_ev_stops = 0
        exposure = copy.copy(center)
        for i in range(num_exposures):
            exposure += ev_step
            running_ev_stops += ev_step
            exposures.append((exposure, running_ev_stops))

        exposures = sorted(exposures)
        comment = str(self.comment)
        for i, (exposure, running_ev_stops) in enumerate(exposures):
            if i == 0:
                self.incremental = "N"
                self.release_command = "TAKEPIC"
            else:
                self.incremental = "Y"
                self.release_command = "TAKEPIC"
            self.comment = f"{comment} {running_ev_stops:+7.3f} EV Stops"
            self.capture(exposure=exposure)
        self.comment = comment

    def __str__(self):
        """
        Verifies all time constraints and writes out csv file that should be
        loadable by Eclipse Orchestrator.
        """
        DATE_FMT = "%Y/%m/%d,%H:%M:%S.%f"
        out = ""
        if self._phase_to_time:
            out = "# Keep these commented out to use the computed contact times of the computer.\n"
            out += "# Add a GPS receiver to get < 1s accurate computed contact times.\n"
            out += "# Event, Date, Time\n"
            out += f"# C1,  {self._c1.strftime(DATE_FMT)}\n"
            out += f"# C2,  {self._c2.strftime(DATE_FMT)}\n"
            out += f"# MAX, {self._max.strftime(DATE_FMT)}\n"
            out += f"# C3,  {self._c3.strftime(DATE_FMT)}\n"
            out += f"# C4,  {self._c4.strftime(DATE_FMT)}\n"

            # Compute max offsets.
            c1_c2_duration = hours_minuts_seconds(self._c2 - self._c1)
            c2_max_duration = hours_minuts_seconds(self._max - self._c2)
            max_c3_duration = hours_minuts_seconds(self._c3 - self._max)
            c3_c4_duration = hours_minuts_seconds(self._c4 - self._c3)

            out += "#\n"
            out += f"# C1:C2  duration: {c1_c2_duration}\n"
            out += f"# C2:MAX duration: {c2_max_duration}\n"
            out += f"# MAX:C3 duration: {max_c3_duration}\n"
            out += f"# C3:4   duration: {c3_c4_duration}\n"
            out += "#\n"

        out += "# Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment\n"

        for event in self._events:
            if isinstance(event, str):
                out += event + "\n"
            else:
                [
                    command,
                    time_offset,
                    phase,
                    camera,
                    exposure,
                    fstop,
                    iso,
                    mirror_lock_up,
                    incremental,
                    comment,
                ] = event

                mlu = mirror_lock_up
                quality = self._qualiy
                sign = "-" if time_offset < 0 else "+"
                hms = hours_minuts_seconds(time_offset)
                exposure = f"{exposure}"
                if command == "RELEASE":
                    out += f"{command},{phase},{sign},{hms},{camera},{exposure:6s},,,,,,,{comment}\n"
                else:
                    out += f"{command},{phase},{sign},{hms},{camera},{exposure:6s},{fstop:4.1f},{iso:4d},{mlu},{quality},None,{incremental},{comment}\n"
        return out

    def save(self, filename):
        with open(filename, "w") as fout:
            fout.write(str(self) + "\n")
        print(f"Wrote {filename}")
