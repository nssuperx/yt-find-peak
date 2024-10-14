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
        tuple[int, ...]: 見つけたピーク時刻
    """
    rate, sound = wavfile.read(f"{filename}.wav")
    sound_l_abs = np.abs(sound[:, 0])
    percentile_height = np.percentile(sound_l_abs, 99.9)
    peaks, _ = find_peaks(sound_l_abs, height=percentile_height, distance=rate * 60)

    # ピーク値が大きい順にする
    desc = np.argsort(sound_l_abs[peaks])[::-1]
    return tuple(int(i) for i in (peaks[desc][:point] // rate))


def find_peak_live_chat(filename: str, point: int) -> tuple[int, ...]:
    """YouTubeのライブチャットのjsonからピークを見つける

    Args:
        filename (str): 拡張子抜きのファイル名(live_chat.jsonファイルを想定)
        point (int): ピーク値取得数

    Returns:
        tuple[int, ...]: 見つけたピーク時刻
    """
    with open(f"{filename}.live_chat.json", encoding="utf-8") as f:
        chat_jsons = (json.loads(line) for line in f)
        timestamps = [
            t.get("replayChatItemAction", {}).get("videoOffsetTimeMsec", 0) for t in chat_jsons
        ]
    timestamps = np.array(timestamps, dtype=np.int32)
    # 0は配信開始前だから抜く
    timestamps = timestamps[timestamps > 0]
    # 秒にする
    timestamps = timestamps / 1000
    # 上記のでfloatになるからintにする
    timestamps = timestamps.astype(np.int32)

    # 1秒ごとのチャット数をカウントしてピーク出す
    counts = np.zeros(timestamps[-1], dtype=np.int32)
    np.add.at(counts, timestamps - 1, 1)
    peaks, _ = find_peaks(counts, distance=60)

    # ピーク値が大きい順にする
    desc = np.argsort(counts[peaks])[::-1]
    return tuple(int(i) for i in peaks[desc][:point])
