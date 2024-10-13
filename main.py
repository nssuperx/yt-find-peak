import sys
import yt_find_peak as yfp
import yt_find_peak.util as yfpu


def main():
    id = sys.argv[1]
    peak_time_sec = yfp.find_peak_sound(id, 5)
    yfpu.gen_concat_csv(peak_time_sec, id)
    peak_time_sec_chat = yfp.find_peak_live_chat(id, 5)
    yfpu.gen_concat_csv(peak_time_sec_chat, id, "-chat", 20, 5)


if __name__ == "__main__":
    main()
