import copy
import dateutil.parser


class Quality:
    raw = "RAW"           # RAW only
    raw_fjpg = "RAW+F-JPG"  # RAW + Fine JPEG

class Dur:
    """Duration"""
    minute = 60.0
    hour = 60 * minute


class Script:
    def __init__(self, c1=None, c2=None, max=None, c3=None, c4=None, minimum_time_step=3.0):
        self._minimum_time_step = minimum_time_step
        self._camera = None
        self._comment = None
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
        self._comment = value

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        self._exposure = value

    @property
    def fstop(self):
        return self._fstop

    @fstop.setter
    def fstop(self, value):
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
        self._iso = value

    @property
    def file_comment(self):
        return None

    @file_comment.setter
    def file_comment(self, comment):
        self._events.append(comment)

    @property
    def release_command(self):
        return self._release_command

    @release_command.setter
    def release_command(self, command):
        assert command in {"TAKEPIC", "RELEASE"}
        self._release_command = command

    def capture(self, abs_time=None, exposure=None):
        # A phase must have been selected.
        assert self._phase, "Phase hasn't been specified!"

        if isinstance(abs_time, str):
            assert abs_time.endswith("PM") or abs_time.endswith("AM"), f"Unexpected time: {abs_time}"
            assert len(abs_time) in {len("HH:MM:SS PM"),len("HH:MM:SS.0 PM")}, f"Unexpected time: {abs_time}"
            assert self._phase_to_time, 'To use HH:MM:SS times, please pass phase times to, i.e. Script(c1 = "YYYY/MM/DD HH:MM:SS.f PM", ...)'
            phase = self._phase_to_time[self._phase]
            time = dateutil.parser.parse(f"{phase.year}/{phase.month}/{phase.day} {abs_time}")
            self.offset = (time - phase).total_seconds()

        exposure = copy.copy(exposure) if exposure else copy.copy(self._exposure)
        if isinstance(exposure, int) or isinstance(exposure, float):
            exposure = Exposure(exposure)

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

        self.offset += float(exposure) + self._minimum_time_step

    def send_exposure(self):
        # A phase must have been selected.
        assert self._phase, "Phase hasn't been specified!"
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
            self._comment,
        ])
        self._incremental = "Y"


    def capture_bracket(self, num_exposures, ev_step=1):
        """
        Catpures a set of bracketed shots centerered on the current exposure
        setting.
        """
        assert num_exposures % 2 == 1, f"num_exposures must be odd, got {num_exposures}"
        assert num_exposures >= 3, f"num_exposures must be >= 3, got {num_exposures}"
        self.incremental = "N"

        center = self._exposure
        exposures = [center]

        # How many faster or slower are left?
        num_exposures -= 1
        num_exposures //= 2
        # Faster exposures.
        exposure = copy.copy(center)
        for i in range(num_exposures):
            exposure -= ev_step
            exposures.append(exposure)

        # Slower exposures.
        exposure = copy.copy(center)
        for i in range(num_exposures):
            exposure += ev_step
            exposures.append(exposure)
        exposures = sorted(exposures)

        self.incremental = "N"
        self.capture(exposure=exposures[0])
        self.incremental = "Y"
        for exposure in exposures[1:]:
            self.capture(exposure=exposure)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        assert value in {"C1", "C2", "MAX", "C3", "C4"}
        self._phase = value

    def __str__(self):
        """
        Verifies all time constraints and writes out csv file that should be
        loadable by Eclipse Orchestrator.
        """
        DATE_FMT = "%Y/%m/%d,%H:%M:%S.%f"
        out = ""
        if self._phase_to_time:
            out = "# Comment out these event times to use GPS time on the laptop\n"
            out += "#Event,Date,Time\n"
            out += f"C1,  {self._c1.strftime(DATE_FMT)}\n"
            out += f"C2,  {self._c2.strftime(DATE_FMT)}\n"
            out += f"MAX, {self._max.strftime(DATE_FMT)}\n"
            out += f"C3,  {self._c3.strftime(DATE_FMT)}\n"
            out += f"C4,  {self._c4.strftime(DATE_FMT)}\n"
        out += "#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment\n"

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
                time_offset = abs(time_offset)
                hours = int(time_offset / Dur.hour)
                time_offset -= Dur.hour * hours
                minutes = int(time_offset / Dur.minute)
                seconds = time_offset - Dur.minute * minutes
                exposure = f"{exposure}"
                out += f"{command},{phase},{sign},{hours:02d}:{minutes:02d}:{seconds:06.3f},{camera},{exposure:6s},{fstop:4.1f},{iso:4d},{mlu},{quality},None,{incremental},{comment}\n"
        return out

    def save(self, filename):
        with open(filename, "w") as fout:
            fout.write(str(self) + "\n")
        print(f"Wrote {filename}")
