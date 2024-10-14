from typing import Iterable
from datetime import timedelta


# 一応このライブラリに含める
def gen_concat_csv(
    peak_time_sec: Iterable[int], filename: str, before: int = 10, after: int = 5
) -> None:
    """切り抜く時刻のcsvファイルを作る

    Args:
        peak_time_sec (Iterable[int]): 切り抜きたい時刻のリストなど
        filename (str): 拡張子抜きのファイル名(csvファイルを想定)
        before (int, optional): 何秒前から切り抜くか. Defaults to 10.
        after (int, optional): 何秒後まで切り抜くか. Defaults to 5.
    """
    peak_time_span = ((t - before, t + after) for t in peak_time_sec)
    time_csv = open(f"{filename}.csv", "w", encoding="utf-8")
    time_csv.write("start,end\n")
    for start, end in peak_time_span:
        time_csv.write(f"{start},{end}\n")
    time_csv.close()


def print_time(peak_time_sec: Iterable[int]) -> None:
    """切り抜き時刻を多少見やすく表示する

    Args:
        peak_time_sec (Iterable[int]): 切り抜きたい時刻のリストなど
    """
    print("time\tseconds\t30fps\t60fps")
    for s in peak_time_sec:
        print(f"{timedelta(seconds=s)}\t{s}\t{s*30}\t{s*60}")
