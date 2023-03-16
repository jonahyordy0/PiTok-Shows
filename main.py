import os

from srnm import TikVideo

import random
import datetime
import time
import shutil
import pickle
from uploader import upload
import datetime

posting_times = {
    0:[
        [5,0],
        [6,0],
        [7,0],
        [10,0],
        [11,0],
        [21,0],
        [22,0],
        [23,0]
    ],
    1:[
        [2,0],
        [3,0],
        [4,0],
        [5,0],
        [8,0]
        [9,0],
        [10,0],
        [12,0]

    ],
    2:[
        [6,0],
        [7,0],
        [8,0],
        [9,0],
        [13,0]
        [22,0],
        [23,0],
        [24,0],
    ],
    3:[
        [9,0],
        [10,0],
        [12,0],
        [13,0],
        [16,0],
        [19,0],
        [20,0],
        [21,0]
    ],
    4:[
        [4,0],
        [5,0],
        [6,0],
        [12,0],
        [13,0],
        [15,0],
        [16,0],
        [21,0]
    ],
    5:[
        [7,0]
        [11,0],
        [12,0],
        [13,0],
        [18,0],
        [19,0],
        [20,0],
        [21,0]
    ],
    6:[
        [7,0],
        [8,0],
        [9,0],
        [12,0],
        [16,0],
        [17,0],
        [21,0],
        [22,0]
    ]
}

post_interval = 8000

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
                #time.sleep(post_interval + random.randint(0, 600))

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
                time_now = datetime.datetime.now()
                if [time_now.hour, time_now.minute] in posting_times[time_now.weekday()]:
                    print("Posting...")
                    cur_video.create_next_clip(clip_len)
                    upload(cname, 2)
                    cur_video.update_info(cur_video.start)
                    #time.sleep(post_interval + random.randint(0, 600))
                time.sleep(15)

            cur_video.destroy()
            time.sleep(10)
    time.sleep(30)