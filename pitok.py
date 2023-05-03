import random
import os
import time
import pickle

from moviepy.editor import *
from moviepy.video.fx.all import crop

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import numpy as np

def create_part_image(part_num):
    text = f'Part {part_num}'

    font = ImageFont.truetype("font.ttf", size=90)
    w, h = font.getsize(text)

    img = Image.new('RGB', (w+30, h+30), (255, 255, 255))
    d = ImageDraw.Draw(img)
    W, H = img.size
    d.text((W/2,H/2), text, fill=(0, 0, 0), font=font, anchor="mm")

    return np.asarray(img)

class TikVideo:
    def __init__(self, loc, clip_name):
        self.loc = loc
        with open('info.pkl', 'rb') as f:
            i = pickle.load(f)
            self.start = i[0]
            self.part = i[1]
        self.clip = VideoFileClip(self.loc)
        self.duration = self.clip.duration
        self.clip_name = clip_name

    def create_next_clip(self, clip_len):
        gp_folder = os.listdir("gameplay")
        random.shuffle(gp_folder)
        clip_len += random.randint(0,20)

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
        
        # Load PIL Part Image
        part_duration = 8
        part_image = ImageClip(create_part_image(self.part), duration=part_duration).margin(top=clip.h, opacity=0)

        # Build our main clip
        video = CompositeVideoClip([gp,clip.set_position(("center","top")), part_image])
        self.start += video.duration
        self.part += 1
        
        # Save as new clip overwritting last one
        video.write_videofile(self.clip_name, preset="ultrafast", fps=30)

        # Close moviepy VideoClip objects to free up memory
        video.close()
        gp.close()
        clip.close()

    
    def update_info(self):
        # Save new start and part value
        with open('info.pkl', 'wb') as f:
            pickle.dump([self.start, self.part], f)

    def is_over(self):
        # Check if the current video is over
        return self.start >= self.duration
    
    def destroy(self):
        # Clear up memory
        os.remove(self.loc)
        self.clip.close()
        with open('info.pkl', 'wb') as f:
            pickle.dump([0, 1], f)
