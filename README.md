# yt-find-peak
YouTubeの動画のいろんなピークを探す

## 環境構築

```bash
pip install -r requirements.txt
```

または

```bash
uv sync --no-dev
```

## 使い方

```bash
python live_chat.py '<動画名>.live_chat.json' 10
```

または

```bash
uv run --no-dev live_chat.py '<動画名>.live_chat.json' 10
```

```text
time    seconds 30fps   60fps
0:08:08 488     14640   29280
0:17:00 1020    30600   61200
0:19:36 1176    35280   70560
0:24:29 1469    44070   88140
0:27:45 1665    49950   99900
0:45:09 2709    81270   162540
0:48:58 2938    88140   176280
1:16:34 4594    137820  275640
1:27:32 5252    157560  315120
1:58:15 7095    212850  425700
```
