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
    def __init__(self, c1, c2, max, c3, c4, minimum_time_step=3.0):
        self._minimum_time_step = minimum_time_step
        self._camera = None
        self._comment = None
        self._events = []
        self._exposure = None
        self._fstop = None
        self._iso = None
        self._phase = None
        self._offset = None
        self._qualiy = Quality.raw_fjpg
        self._mirror_lock_up = 0.0  # Mirrorless cameras don't have a mirror!
        self._incremental = 'N' # Only changes in camera settings and transmitted via USB.
        self._c1 = dateutil.parser.parse(c1)
        self._c2 = dateutil.parser.parse(c2)
        self._max = dateutil.parser.parse(max)
        self._c3 = dateutil.parser.parse(c3)
        self._c4 = dateutil.parser.parse(c4)
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

    def capture(self, abs_time=None, exposure=None):
        # A phase must have been selected.
        assert self._phase, "Phase hasn't been specified!"

        if isinstance(abs_time, str):
            assert abs_time.endswith("PM") or abs_time.endswith("AM"), f"Unexpected time: {abs_time}"
            assert len(abs_time) in {len("HH:MM:SS PM"),len("HH:MM:SS.0 PM")}, f"Unexpected time: {abs_time}"
            phase = self._phase_to_time[self._phase]
            time = dateutil.parser.parse(f"{phase.year}/{phase.month}/{phase.day} {abs_time}")
            self.offset = (time - phase).total_seconds()

        exposure = copy.copy(exposure) if exposure else copy.copy(self._exposure)
        if isinstance(exposure, int):
            exposure = Exposure(exposure)

        self._events.append([
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

        self.offset += max(self._minimum_time_step, exposure)

    def capture_bracket(self, num_exposures, ev_step=1):
        """
        Catpures a set of bracketed shots centerered on the current exposure
        setting.
        """
        assert num_exposures % 2 == 1, f"num_exposures must be odd, got {num_exposures}"
        assert num_exposures >= 3, f"num_exposures must be >= 3, got {num_exposures}"
        self.incremental = "N"
        # Centered shot.
        self.capture()
        self.incremental = "Y"

        # How many faster or slower are left?
        num_exposures -= 1
        num_exposures //= 2

        # Faster exposures.
        exposure = copy.copy(self._exposure)
        for i in range(num_exposures):
            exposure -= ev_step
            self.capture(exposure=exposure)

        # Slower exposures.
        exposure = copy.copy(self._exposure)
        for i in range(num_exposures):
            exposure += ev_step
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

    def save(self, filename):
        """
        Verifies all time constraints and writes out csv file that should be
        loadable by Eclipse Orchestrator.
        """
        DATE_FMT = "%Y/%m/%d,%H:%M:%S.%f"
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
                out += f"TAKEPIC,{phase},{sign},{hours:02d}:{minutes:02d}:{seconds:04.1f},{camera},{exposure},{fstop:4.1f},{iso:4d},{mlu},{quality},None,{incremental},{comment}\n"

        with open(filename, "w") as fout:
            fout.write(out)

        print(f"Wrote {filename}")
