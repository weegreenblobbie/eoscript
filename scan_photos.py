import argparse
import glob
import os.path

# pip install exifread
import exifread
# pip install python-dateutil
import dateutil.parser


def get_timestamp_nikon(tags):
    date, time = str(tags['Image DateTimeOriginal']).split(" ")
    date = date.replace(":", "-")
    frac_sec = int(tags['EXIF SubSecTime'].values)

    local_time = dateutil.parser.parse(
        f"{date} {time}.{frac_sec:03d}",
        #tzinfos={"PST":dateutil.tz.gettz("America/Los_Angeles")},
    )

    return local_time


def get_timestamp_sony(tags):
    date, time = str(tags['EXIF DateTimeOriginal']).split(" ")
    date = date.replace(":", "-")
    frac_sec = 0

    local_time = dateutil.parser.parse(
        f"{date} {time}.{frac_sec:03d}",
        #tzinfos={"PST":dateutil.tz.gettz("America/Los_Angeles")},
    )

    return local_time


def get_timeoffset(time, reference):

    time_offset = (time - reference).total_seconds()

    sign = "-" if time_offset < 0 else "+"
    time_offset = abs(time_offset)
    hours = int(time_offset / 3600.0)
    time_offset -= 3600.0 * hours
    minutes = int(time_offset / 60.0)
    seconds = time_offset - 30.0 * minutes
    return f"{sign},{hours:02d}:{minutes:02d}:{seconds:06.3f}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    args = parser.parse_args()
    assert os.path.isdir(args.input_dir), f"Dir not found: {args.input_dir}"

    print(f"{'Filename':32s}, {'Offset':13s}, Campera, Exposure, Fstop, ISO, Quality")

    files = sorted(glob.glob(os.path.join(args.input_dir, "*")))
    data = []
    time_ref = None
    count = 0

    for filename in files:
        with open(filename, 'rb') as fin:
            tags = exifread.process_file(fin)

        if not tags:
            continue

        make = tags["Image Make"].values.lower()

        if "sony" in make:
            timestamp = get_timestamp_sony(tags)
        elif "nikon" in make:
            timestamp = get_timestamp_nikon(tags)
        else:
            raise ValueError(f"Don't know how to read {make}")

        if time_ref is None:
            time_ref = timestamp

        time_offset = get_timeoffset(timestamp, time_ref)
        camera = tags['Image Model']
        exposure = tags['EXIF ExposureTime']
        iso = tags['EXIF ISOSpeedRatings']
        fstop = tags['EXIF FNumber']
        quality = tags.get('MakerNote Quality', "???")

        exposure = str(exposure)
        fstop = str(fstop)
        iso = str(iso)

        print(f"{filename:40s}, {time_offset}, {camera}, {exposure:6s}, {fstop:4s}, {iso:4s}, {quality}")

        time_ref = timestamp
        count += 1

    print(f"{count} files")


if __name__ == "__main__":
    main()