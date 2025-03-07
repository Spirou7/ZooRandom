import requests
import m3u8
import cv2
import os

# HLS .m3u8 URL (replace with your own)
m3u8_url = "https://zssd-penguin.hls.camzonecdn.com/CamzoneStreams/zssd-penguin/Playlist.m3u8"

# Function to download the latest .ts file
def get_latest_ts_file(m3u8_url):
    response = requests.get(m3u8_url)
    if response.status_code != 200:
        print("Failed to fetch .m3u8 file")
        return None

    # Parse the .m3u8 playlist
    playlist = m3u8.loads(response.text)

    # Get the last segment URL (latest one)
    if not playlist.segments:
        print("No segments found in the playlist")
        return None

    latest_segment = playlist.segments[-1].uri  # Last segment
    ts_url = latest_segment if latest_segment.startswith("http") else os.path.join(os.path.dirname(m3u8_url), latest_segment)

    print(f"Latest TS file URL: {ts_url}")

    # Download the .ts file
    ts_response = requests.get(ts_url, stream=True)
    if ts_response.status_code == 200:
        with open("latest.ts", "wb") as f:
            f.write(ts_response.content)
        return "latest.ts"
    else:
        print("Failed to download .ts file")
        return None

# Function to extract a frame from the .ts file
def extract_frame(ts_file, output_image="frame.jpg"):
    cap = cv2.VideoCapture(ts_file)

    if not cap.isOpened():
        print("Error: Could not open video file")
        return False

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_image, frame)
        print(f"Frame saved as {output_image}")
        cap.release()
        return True
    else:
        print("Error: Could not read frame")
        cap.release()
        return False

# Main script execution
ts_file = get_latest_ts_file(m3u8_url)
if ts_file:
    extract_frame(ts_file)

