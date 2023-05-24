import os

from pitok import TikVideo

import random
import datetime
import time
import shutil
import pickle
from uploader import upload
import datetime

posting_times = {
    0:[ # Monday
        [6,0],
        [10,0],
        [22,0],

        [13,0],
        [18,0]
    ],
    1:[ # Tuesday
        [2,0],
        [4,0],
        [9,0],

        [14,0],
        [20,0]

    ],
    2:[ # Wednesday
        [7,0],
        [8,0],
        [23,0],

        [13,0],
        [18,0]
    ],
    3:[ # Thursday
        [9,0],
        [12,0],
        [19,0],

        [23,0],
        [20,0]
    ],
    4:[ # Friday
        [5,0],
        [13,0],
        [15,0],

        [9,0],
        [23,0]
    ],
    5:[ # Saturday
        [11,0],
        [19,0],
        [20,0],

        [15,0],
        [6,0]
    ],
    6:[ #Sunday
        [7,0],
        [8,0],
        [16,0],

        [22,0],
        [12,0]
    ]
}

while True:
    drives = os.listdir("/media/"+ os.getlogin() +"/")
    print(drives)
    if len(drives) == 0:
        print("No drives detected")


    elif drives[0] == "RNM":
        # Set constants for rick and morty account
        clip_len = 65
        vname = "curClip.mp4"
        #cname = "#rick #rickandmorty #foryou #fyp #morty #movie #game #❤️❤️.mp4"
        cname = "#fypシ #tiktok #viral #gameplay #mobilegame #rickandmorty #rick #morty.mp4"

        videos_folder = os.listdir("/media/"+ os.getlogin() +"/"+drives[0]+"/videos")

        # Loop through all videos on drive
        while len(videos_folder) > 0:
            # Check if we are already editing a video
            if not os.path.isfile(vname):
                # Move new video from drive to local folder saved as name (vname)
                cur_file = videos_folder[0]
                shutil.move("/media/"+ os.getlogin() +"/"+drives[0]+"/videos/" + cur_file, "./" + vname)

                # Reset pickle file
                with open("info.pkl", "wb") as f:
                    pickle.dump([0, 1], f)

            # Init tik tok video object
            cur_video = TikVideo(vname, cname)
            print(cur_video.start)

            # Continue posting clips until entire video is posted
            while not cur_video.is_over():
                # Get the current time to check if it is time to post
                time_now = datetime.datetime.now()
                print(time_now)

                if [time_now.hour, time_now.minute] in posting_times[time_now.weekday()]:
                    print("Posting...")
                    # Create next clip and upload
                    cur_video.create_next_clip(clip_len)
                    upload(cname, 2)
                    # Set new start point for next clip
                    cur_video.update_info()

                time.sleep(15)

            # Delete local video file and destroy movie py objects to free up memory
            cur_video.destroy()
            videos_folder = os.listdir("/media/"+ os.getlogin() +"/"+drives[0]+"/videos")
            time.sleep(10)

    time.sleep(30)
