from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from bs4 import BeautifulSoup
import random
import glob
from moviepy.editor import VideoFileClip, AudioFileClip

audio_filenames = glob.glob("audios/*.mp3")

keyword = input("Enter the keyword of videos: ")
num_videos = input("Enter the number of videos to download: ")

# fetch the HTML from the webpage
req = Request(
    url="https://www.pexels.com/search/videos/" + keyword + "/?orientation=portrait&size=small" ,#small, medium
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
)
html = urlopen(req).read()

# parse the HTML to find the links to the videos
soup = BeautifulSoup(html, "html.parser")
video_links = []
for link in soup.find_all("a"):
    if link.get("title") == "Download":
      video_links.append(link.get("href"))

opener = build_opener()
opener.addheaders = [
  ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
  ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
  ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
  ('Accept-Encoding', 'none'),
  ('Accept-Language', 'en-US,en;q=0.8'),
  ('Connection', 'keep-alive')]
install_opener(opener)

# download the videos
for i, link in enumerate(video_links):
    if i >= int(num_videos):
        break
    urlretrieve(link, "videos/video_" + str(i) + ".mp4")
    print("Downloaded video " + str(i) + "")
    video = VideoFileClip("videos/video_" + str(i) + ".mp4")
    audio_filename = random.choice(audio_filenames)
    print("audio_filename", audio_filename)
    audio = AudioFileClip(audio_filename)
    audio = audio.set_fps(44100)
    video = video.set_audio(audio)
    output = video.set_duration(video.duration)
    output.write_videofile("result/video_" + str(i) + "_" + keyword + ".mp4")
    print("Added audio to video {}")

