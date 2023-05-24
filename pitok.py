import random
import os
import time
import pickle

from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.audio.fx.volumex import volumex

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import numpy as np

def create_part_image(part_num):
    text = f'Part {part_num}'

    font = ImageFont.truetype("font.ttf", size=60)
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
        clip = VideoFileClip(self.loc)
        gp_folder = os.listdir("gameplay")
        random.shuffle(gp_folder)
        clip_len += random.randint(0,20)
        top_margin = 200

        # Gameplay variables
        gp_num = 0
        gp_dur = 0
        gp_clips = []

        # Check if clip is nearing end so last clip isn't only a few seconds long
        if self.duration < (self.start + clip_len + 20):
            clip = clip.subclip(self.start, self.duration).resize(width=720).margin(top=top_margin).afx(volumex, 15)
        else:
            clip = clip.subclip(self.start, self.start + clip_len).resize(width=720).margin(top=top_margin).afx(volumex, 15)

        # Build gameplay same length as our clip
        while gp_dur < clip.duration:
            temp_clip = VideoFileClip("gameplay/" +gp_folder[gp_num]).without_audio()
            (w, h) = temp_clip.size
            temp_clip = crop(temp_clip, height=h - top_margin,y_center=h/2 - 50)
            temp_clip = temp_clip.margin(top=top_margin)

            gp_dur += temp_clip.duration
            gp_clips.append(temp_clip)
            gp_num+=1

        # Chop access gameplay and combine
        gp_clips[-1] = gp_clips[-1].subclip(0, gp_clips[-1].duration - (gp_dur - clip.duration))
        gp_dur -= clip.duration
        gp = concatenate_videoclips(gp_clips)
        # Load PIL Part Image
        part_duration = 7
        part_image = ImageClip(create_part_image(self.part), duration=part_duration).margin(top=clip.h, opacity=0)

        # Build our main clip
        video = CompositeVideoClip([gp,clip.set_position(("center","top")), part_image.set_position(("center", "top"))])
        self.start += video.duration
        self.part += 1

        # Save as new clip overwritting last one
        video.write_videofile(self.clip_name, preset="ultrafast", fps=30)

        # Close moviepy VideoClip objects to free up memory
        video.close()
        gp.close()
        clip.close()
        temp_clip.close()
        part_image.close()

        # Close indivdual gameplay clips
        for c in gp_clips:
            c.close()


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
