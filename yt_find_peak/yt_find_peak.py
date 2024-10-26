import json
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks


def find_peak_sound(filename: str, point: int) -> tuple[int, ...]:
    """音声ファイルからピークを見つける

    Args:
        filename (str): 拡張子抜きのファイル名(wavファイルを想定)
        point (int): ピーク値取得数

    Returns:
        tuple[int, ...]: 音量が大きい時刻
    """
    rate, sound = wavfile.read(f"{filename}.wav")
    # 後で適当に足すので、int64にする
    sound = sound.astype(np.int64)
    sound = sound[(sound.shape[0] % rate) // 2 : -(sound.shape[0] % rate) // 2]
    # 左右の音を足す
    sound = np.abs(sound[:, 0]) + np.abs(sound[:, 1])
    # rateずつ分けて足す（適当に平均化してる）
    sound = sound.reshape((-1, rate)).sum(axis=1)
    percentile_height = np.percentile(sound, 97)
    peaks, _ = find_peaks(sound, height=percentile_height, distance=60)

    # ピーク値が大きい順にする
    desc = np.argsort(sound[peaks])[::-1]
    return tuple(int(i) for i in (peaks[desc][:point]))


def find_peak_live_chat(filename: str, point: int) -> tuple[int, ...]:
    """YouTubeのライブチャットのjsonからコメント数が多い時刻を見つける

    Args:
        filename (str): 拡張子抜きのファイル名(live_chat.jsonファイルを想定)
        point (int): ピーク値取得数

    Returns:
        tuple[int, ...]: コメント数が多い時刻
    """
    with open(f"{filename}.live_chat.json", encoding="utf-8") as f:
        chat_jsons = (json.loads(line) for line in f)
        timestamps = [t.get("replayChatItemAction", {}).get("videoOffsetTimeMsec", 0) for t in chat_jsons]
    timestamps = np.array(timestamps, dtype=np.int32)
    # 0は配信開始前だから抜く
    timestamps = timestamps[timestamps > 0]
    # 秒にする
    timestamps = timestamps / 1000
    # 上記のでfloatになるからintにする
    timestamps = timestamps.astype(np.int32)

    # 1秒ごとのチャット数をカウントしてピーク出す
    counts = np.zeros(timestamps[-1] + 1, dtype=np.int32)
    np.add.at(counts, timestamps, 1)
    peaks, _ = find_peaks(counts, distance=60)

    # ピーク値が大きい順にする
    desc = np.argsort(counts[peaks])[::-1]
    return tuple(int(i) for i in peaks[desc][:point])


def find_peak_heatmap(filename: str, point: int) -> tuple[int, ...]:
    """youtube-dlの--write-info-jsonして取得できるファイルから
    ヒートマップの値を見て大きい時刻を取得する

    Args:
        filename (str): 拡張子抜きのファイル名(info.jsonファイルを想定)
        point (int): ピーク値取得数

    Returns:
        tuple[int, ...]: ヒートマップの値が大きい時刻
    """
    with open(f"{filename}.info.json", encoding="utf-8") as f:
        heatmap = json.load(f)["heatmap"]

    # 一回全部ndarrayにする
    raw = np.array(
        [(float(v.get("start_time", 0)), float(v.get("end_time", 0)), float(v.get("value", 0))) for v in heatmap],
        dtype=np.float32,
    )

    # 最初はvalueが1だから除外
    raw = raw[1:]
    # start_time < end_time かつ heatmapの値が0より大きいなら有効（これでFalseになる値はほぼないと思うけど）
    valid = raw[(raw[:, 0] < raw[:, 1]) & (raw[:, 2] > 0.0)]
    time_value = np.array([(valid[:, 1] + valid[:, 0]) * 0.5, valid[:, 2]]).T

    peaks, _ = find_peaks(time_value[:, 1])

    # ピーク値が大きい順にする
    peak_time_value = time_value[peaks]
    desc = np.argsort(peak_time_value[:, 1])[::-1]
    return tuple(int(i) for i in peak_time_value[:, 0][desc][:point])
