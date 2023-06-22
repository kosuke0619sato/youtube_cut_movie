import os
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import concatenate_videoclips, VideoFileClip
import openai
import youtube_dl

# YouTubeから字幕を抽出
video_id = "ViBoy6YZ3Gc"
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

# 字幕データをテキスト形式に変換
transcript_text = ' '.join([x['text'] for x in transcript_list])

# GPT-4で面白い部分を抽出
openai.api_key = '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'
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=transcript_text,
    temperature=0.5,
    max_tokens=100
)

# 面白い部分を抽出 (ここでは適当な処理をしています。実際には適切な処理を設定する必要があります)
interesting_parts = response.choices[0].text.strip().split('\n')

# 動画のダウンロード
ydl_opts = {'outtmpl':'/Users/kosuke/Downloads/python_work/private/%(title)s-%(id)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info('https://www.youtube.com/watch?v=ViBoy6YZ3Gc', download=True)
video_path = ydl.prepare_filename(info_dict)  # ダウンロードした動画のパスを取得

# 動画から面白い部分を切り抜き
clips = []
for part in interesting_parts:
    start_time, end_time = part.split('-')  # 面白い部分の開始時間と終了時間を取得する処理を設定する必要があります
    clip = VideoFileClip(video_path).subclip(int(start_time), int(end_time))  # ダウンロードした動画のパスを指定
    clips.append(clip)

# 切り抜いた部分を連結
final_clip = concatenate_videoclips(clips)

# 新しい動画を出力
final_clip.write_videofile("output.mp4")

