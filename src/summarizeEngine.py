# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:35:23 2023

@author: Oscar Sapena
"""
from googletrans import Translator
import spacy
import json
import os
from moviepy.editor import VideoFileClip

class SummarizeEngine:
    
    def __init__(self):
        """
        Inicialización del motor de búsqueda basado en resúmenes de video
        """
            
        print('Loading videos...')      
        self.summaries = []
        self.videos = []
        vlist = os.listdir('examples')
        for video in vlist:
            
            filename = video[:-4]
            print(video)
            video_clip = VideoFileClip('examples/'+video)
            self.videos.append(video_clip)
        print(f'\t{len(self.videos)} videos loaded')

