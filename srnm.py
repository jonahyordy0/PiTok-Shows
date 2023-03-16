import random
import os
import time
import pickle

from moviepy.editor import *
from moviepy.video.fx.all import crop

class TikVideo:
    def __init__(self, loc, clip_name):
        self.loc = loc
        with open('info.pkl', 'rb') as f:
            self.start = pickle.load(f)
        self.clip = VideoFileClip(self.loc)
        self.duration = self.clip.duration
        self.clip_name = clip_name

    def create_next_clip(self, clip_len):
        clip_len += random.randint(-7,12)
        gp_folder = os.listdir("gameplay")
        random.shuffle(gp_folder)

        # Gameplay variables
        gp_num = 0
        gp_dur = 0
        gp_clips = []
        
        # Check if clip is nearing end so last clip isn't only a few seconds long
        if self.duration < (self.start + clip_len + 20):
            clip = self.clip.subclip(self.start, self.duration).resize(width=720).margin(top=100)
        else:
            clip = self.clip.subclip(self.start, self.start + clip_len).resize(width=720).margin(top=100)
        
        # Build gameplay same length as our clip
        while gp_dur < clip.duration:
            temp_clip = VideoFileClip("gameplay/" +gp_folder[gp_num]).without_audio()
            (w, h) = temp_clip.size
            temp_clip = crop(temp_clip, height=h - 100,y_center=h/2 - 50)
            temp_clip = temp_clip.margin(top=100)

            gp_dur += temp_clip.duration
            gp_clips.append(temp_clip)
            gp_num+=1
            temp_clip.close()

        # Chop access gameplay and combine
        gp_clips[-1] = gp_clips[-1].subclip(0, gp_clips[-1].duration - (gp_dur - clip.duration))
        gp_dur -= clip.duration
        gp = concatenate_videoclips(gp_clips)

        # Close indivdual gameplay clips
        for c in gp_clips:
            c.close()
        
        # Build our main clip
        video = CompositeVideoClip([gp,clip.set_position(("center","top"))])
        self.start += video.duration
        
        # Save as new clip overwritting last one
        video.write_videofile(self.clip_name, preset="ultrafast")

        # Close moviepy VideoClip objects to free up memory
        video.close()
        gp.close()

    
    def update_info(self, start):
        # Save new start value
        with open('info.pkl', 'wb') as f:
            pickle.dump(start, f)

    def is_over(self):
        # Check if the current video is over
        return self.start >= self.duration
    
    def destroy(self):
        # Clear up memory
        os.remove(self.loc)
        self.clip.close()
        with open('info.pkl', 'wb') as f:
            pickle.dump(0, f)
