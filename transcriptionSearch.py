# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 19:54:51 2023

@author: Oscar
"""
from transcriptionEngine import TranscriptionEngine

if __name__ == '__main__':
    engine = TranscriptionEngine()
    sentence = input('Enter your search: ')
    while sentence != '': # Empty string to finish
        bestVideos = engine.searchBestVideos(sentence)
        for video, score, _ in bestVideos:
            print(f'{score:.<8.3f}{video}')
        if len(bestVideos) > 0 and bestVideos[0][1] > 0.001:
            video, _, videoIndex = bestVideos[0]
            print('BEST SCENES:')
            best_scenes = engine.searchBestScenes(videoIndex)
            for start, end, text, score in best_scenes:
                print(f'{score:.<8.3f}: {start} -> {end}')
                print(text)
        print()
        sentence = input('Enter your search: ')
