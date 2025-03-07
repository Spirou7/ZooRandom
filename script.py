import requests
import ffmpeg
import os

# Step 1: Define the M3U8 URL
M3U8_URL = "https://zssd-penguin.hls.camzonecdn.com/CamzoneStreams/zssd-penguin/chunklist.m3u8"  # Change this to your actual URL

def get_ts_urls(m3u8_url):
    # Step 2: Fetch the M3U8 playlist
    response = requests.get(m3u8_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch M3U8 file")

    # Step 3: Parse the first TS segment URL
    base_url = m3u8_url.rsplit("/", 1)[0]  # Extract base URL
    lines = response.text.splitlines()

    ts_urls = []
    for line in lines:
        if(line.endswith(".ts")):
            ts_url = f"{base_url}/{line}"
            ts_urls.append(ts_url)
    
    return ts_urls


def download_ts(ts_url, ts_filename):
    # this makes a web request to the ts url, and then writes it to the filename
    with requests.get(ts_url, stream=True) as r:
        r.raise_for_status()
        with open(ts_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def get_frame_from_ts(ts_filename, output_frame):
    ffmpeg.input(ts_filename).output(output_frame, vframes=1, ss=1, y=None).run()

def delete_ts(ts_filename):
    os.remove(ts_filename)





ts_urls = get_ts_urls(M3U8_URL)

ts_filename = "segment.ts"
download_ts(ts_urls[0], ts_filename)

output_frame = "outputs/frame.jpg"
get_frame_from_ts(ts_filename, output_frame)

delete_ts(ts_filename)
