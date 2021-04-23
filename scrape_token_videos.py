import requests
from bs4 import BeautifulSoup
import cv2
import urllib.request
import os, shutil
import uuid

variant_id = 376 # walk
#variant_id = 527 # bat
output_folder = "processed_frames"
hand_sign_label = "bat"

save_dir = "{}\\".format(output_folder)

prefix_url = "https://dai.cs.rutgers.edu/dai/s/"
page = requests.get('http://dai.cs.rutgers.edu/dai/s/occurrence?id_SignBankVariant=' + str(variant_id))
soup = BeautifulSoup(page.content, 'html.parser')
vid = soup.find_all(id="videoview")
video_links = []
for i in vid:
    onclick_text = i.get('onclick')
    video_link = onclick_text[onclick_text.find("\'")+1:onclick_text.rfind("\'")]
    # Avoids the vidoes with type T where the background have been removed.
    if not video_link.endswith("T"):
        full_video_link = prefix_url + video_link
        video_links.append(full_video_link)

for link in video_links:
    video_page = requests.get(link)
    video_soup = BeautifulSoup(video_page.content, 'html.parser')
    tags = video_soup.find_all('video')
    children = tags[0].findChildren("source" , recursive=False)
    link = children[0].get('src')
    uid = uuid.uuid1()
    urllib.request.urlretrieve(link, 'temp_videos\\{}.mp4'.format(uid))
    
    # Converts downloaded video to frames
    vidcap = cv2.VideoCapture('temp_videos\\{}.mp4'.format(uid))
    success, image = vidcap.read()
    count = 0
    # Saves all frames from videos in the a folder for it's category.
    frames_save_dst = save_dir + hand_sign_label
    if not os.path.exists(frames_save_dst):
        os.makedirs(frames_save_dst)
    while success:
        cv2.imwrite(frames_save_dst + "\{}.jpg".format(uuid.uuid1()), image)   
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
