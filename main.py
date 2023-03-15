import os

#import syoutube
from srnm import TikVideo
#import ssp

import random
import time
import shutil
import pickle
from uploader import upload

drives = os.listdir("/media/jonah/")

if len(drives) == 0:
    print("No drives detected")

elif drives[0] == "YOUTUBE":

    pass

elif drives[0] == "RNM":
    clip_len = 46
    cname = "#rick #rickandmorty #foryou #fyp #morty #movie #game #❤️❤️.mp4"
    videos_folder = os.listdir("/media/jonah/RNM/videos")

    while len(videos_folder) > 0:
        videos_folder = os.listdir("/media/jonah/RNM/videos")
        if not os.path.isfile("curClip.mp4"):
            cur_file = videos_folder[0]
            shutil.move("/media/jonah/RNM/videos/" + cur_file, "./curClip.mp4")
            with open("info.pkl", "wb") as f:
                pickle.dump(0, f)

        cur_video = TikVideo('curClip.mp4', cname)
        print(cur_video.start)
        
        while not cur_video.is_over():
            cur_video.create_next_clip(clip_len)
            upload(cname, 2)
            cur_video.update_info(cur_video.start)
            time.sleep(6000 + random.randint(0, 600))

        cur_video.destroy()
        time.sleep(10)
    