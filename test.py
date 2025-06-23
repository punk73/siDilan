import subprocess
import cv2
import numpy as np

stream_url = "https://cctv.purwakartakab.go.id/streams/perempatan-pemda.m3u8"

headers = (
    'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36\r\n'
    'Referer: https://cctv.purwakartakab.go.id/node/pertigaan-sasak-beusi\r\n'
    'Cookie: _clck=1911zsg%7C2%7Cfwv%7C0%7C1973; _clsk=1yzqwv2%7C1750227793851%7C3%7C1%7Cl.clarity.ms%2Fcollect\r\n'
)

command = [
    "ffmpeg",
    "-headers", headers,
    "-i", stream_url,
    "-loglevel", "quiet",
    "-an",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-"
]

width = 640
height = 360
pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)

while True:
    raw_image = pipe.stdout.read(width * height * 3)
    if len(raw_image) != width * height * 3:
        print("⚠️ Failed to read frame from stream.")
        break

    frame = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 3))
    cv2.imshow("CCTV Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipe.terminate()
cv2.destroyAllWindows()