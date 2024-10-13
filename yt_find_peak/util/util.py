from typing import Iterable


# 一応このライブラリに含める
def gen_concat_csv(
    peak_time_sec: Iterable[int], id: str, postfix: str = "", before: int = 10, after: int = 5
) -> None:
    peak_time_span = ((t - before, t + after) for t in peak_time_sec)
    time_csv = open(f"{id}{postfix}.csv", "w", encoding="utf-8")
    time_csv.write("start,end\n")
    for start, end in peak_time_span:
        time_csv.write(f"{start},{end}\n")
    time_csv.close()
