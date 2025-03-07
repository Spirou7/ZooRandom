import requests
import ffmpeg
import os

# Step 1: Define the M3U8 URL
M3U8_URL = "https://zssd-penguin.hls.camzonecdn.com/CamzoneStreams/zssd-penguin/chunklist.m3u8"  # Change this to your actual URL

# Step 2: Fetch the M3U8 playlist
response = requests.get(M3U8_URL)
if response.status_code != 200:
    raise Exception("Failed to fetch M3U8 file")

# Step 3: Parse the first TS segment URL
base_url = M3U8_URL.rsplit("/", 1)[0]  # Extract base URL
lines = response.text.splitlines()
ts_file = next(line for line in lines if line.endswith(".ts"))  # Get first .ts file
ts_url = f"{base_url}/{ts_file}"

# Step 4: Download the TS file
ts_filename = "segment.ts"
with requests.get(ts_url, stream=True) as r:
    r.raise_for_status()
    with open(ts_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print(f"Downloaded {ts_filename}")

# Step 5: Extract a frame using FFmpeg
output_frame = "frame.jpg"
ffmpeg.input(ts_filename).output(output_frame, vframes=1, ss=1, y=None).run()

print(f"Extracted frame saved as {output_frame}")

# Clean up
os.remove(ts_filename)

