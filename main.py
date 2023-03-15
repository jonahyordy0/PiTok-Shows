import os

#import syoutube
from srnm import TikVideo
#import ssp

import random
import time
import shutil
import pickle
from uploader import upload


while True:
    drives = os.listdir("/media/"+ os.getlogin() +"/")
    print(drives)
    if len(drives) == 0:
        print("No drives detected")

    elif drives[0] == "SOUTHPARK":
        clip_len = 44
        vname = "curClip.mp4"
        cname = "#cartman #southpark #foryou #fyp #kenny #kyle #game.mp4"
        videos_folder = os.listdir("/media/"+ os.getlogin() +"/SOUTHPARK/videos")

        while len(videos_folder) > 0:
            videos_folder = os.listdir("/media/"+ os.getlogin() +"/SOUTHPARK/videos")
            if not os.path.isfile(vname):
                cur_file = videos_folder[0]
                shutil.move("/media/"+ os.getlogin() +"/SOUTHPARK/videos/" + cur_file, "./" + vname)
                with open("info.pkl", "wb") as f:
                    pickle.dump(0, f)

            cur_video = TikVideo(vname, cname)
            print(cur_video.start)
            
            while not cur_video.is_over():
                cur_video.create_next_clip(clip_len)
                upload(cname, 3)
                cur_video.update_info(cur_video.start)
                time.sleep(6000 + random.randint(0, 600))

            cur_video.destroy()
            time.sleep(10)
            
    elif drives[0] == "YOUTUBE":
        clip_len = 65
        cname = "#youtube #youtubeclips #foryou #fyp #trending #movie #game #viral.mp4"

    elif drives[0] == "RNM":
        clip_len = 46
        vname = "curClip.mp4"
        cname = "#rick #rickandmorty #foryou #fyp #morty #movie #game #❤️❤️.mp4"
        videos_folder = os.listdir("/media/"+ os.getlogin() +"/RNM/videos")

        while len(videos_folder) > 0:
            videos_folder = os.listdir("/media/"+ os.getlogin() +"/RNM/videos")
            if not os.path.isfile(vname):
                cur_file = videos_folder[0]
                shutil.move("/media/"+ os.getlogin() +"/RNM/videos/" + cur_file, "./" + vname)
                with open("info.pkl", "wb") as f:
                    pickle.dump(0, f)

            cur_video = TikVideo(vname, cname)
            print(cur_video.start)
            
            while not cur_video.is_over():
                cur_video.create_next_clip(clip_len)
                upload(cname, 2)
                cur_video.update_info(cur_video.start)
                time.sleep(6000 + random.randint(0, 600))

            cur_video.destroy()
            time.sleep(10)
    time.sleep(30)