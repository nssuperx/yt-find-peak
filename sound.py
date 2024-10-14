import sys
import pathlib
import yt_find_peak as yfp
import yt_find_peak.util as yfpu


def main():
    file = pathlib.Path(sys.argv[1])
    point = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    peak_time_sec = yfp.find_peak_sound(file.stem, point)
    yfpu.print_time(peak_time_sec)


if __name__ == "__main__":
    main()
