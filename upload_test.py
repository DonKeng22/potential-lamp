import requests

url = "http://localhost:8000/streams/upload-video"
files = {'file': open('C:/Users/devai/OSKED00/potential-lamp/dummy_video.mp4', 'rb')}

try:
    response = requests.post(url, files=files)
    print(response.json())
except Exception as e:
    print(f"An error occurred: {e}")
