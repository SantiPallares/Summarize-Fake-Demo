# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:35:23 2023

@author: Oscar Sapena
"""
from googletrans import Translator
import spacy
import json
import os

class TranscriptionEngine:
    
    def __init__(self):
        """
        Inicialización del motor de búsqueda basado en transcripciones
        """
        print('Loading translator...')
        self.translator = Translator()      # Google translator
        print('Loading language model...')
        model = 'en_core_web_trf'
        self.nlp = spacy.load(model)        # Tokenizer
        print('Loading videos...')          # Videos
        self.summaries = []
        self.topics = []
        self.videos = []
        self.scenes = []
        self.scenesPerTopic = []
        vlist = os.listdir('src/lda/')
        for video in vlist:
            if video.endswith('.json'):
                filename = video[:-5]
                with open(f'src/lda/{video}', 'r') as f:
                   doc = json.load(f)
                for chunk in doc['chunks']:
                    chunk['keywords'] = set(chunk['keywords'])
                self.summaries.append(doc['summary'])
                self.topics.append(doc['topics'])
                self.scenes.append(doc['chunks'])
                self.scenesPerTopic.append(doc['scenes'])
                self.videos.append(filename)
        print(f'\t{len(self.videos)} videos loaded')
        print('Loading synonyms...')
        with open('src/synonyms.json', 'r') as f:
            self.synonyms = json.load(f)
        print('Loading bigrams...')
        with open('src/bigrams.json', 'r') as f:
            self.bigrams = json.load(f)
        self.keywords = []

    def searchBestVideos(self, sentence, top = 5):
        """
        Busca los vídeos que mejor se corresponden con la frase recibida.
        Parameters
        ----------
        sentence : str
            Frase a buscar.
        top : int, optional
            Número de vídeos a devolver.

        Returns
        -------
        Lista de tuplas (nombre_del_vídeo, similitud, índice_del_vídeo).
        """
        translated = self.translator.translate(sentence, dest='en').text
        doc = self.nlp(translated)
        tokens =  [(token.text.lower(), token.lemma_.lower(), token.pos_)
                   for token in doc]
        self.keywords = self.__labelVideoSenses(tokens)
        self.keywords.extend([f'{w.text.lower()}:{w.label_}'
                              for w in doc.ents])
        result = []
        for i in range(len(self.videos)):
            score = self.__evaluate(self.keywords, self.summaries[i])
            result.append((self.videos[i], score, i))
        sorted_result = sorted(result, key=lambda x:x[1], reverse=True)
        return sorted_result[:top]
    
    def searchBestScenes(self, numVideo, top = 5):
        """
        Devuelve las escenas del vídeo indicado que mejor se corresponden
        con la frase indicada en el método anterior (searchBestVideos).
        Parameters
        ----------
        numVideo : int
            Índice el vídeo donde buscar las escenas.
        top : int, optional
            Número de escenas a devolver.

        Returns
        -------
        Lista de tuplas (tiempo_inicio, tiempo_fin, texto, simulitud).
        """
        result = []
        topicId = 0
        for sc in self.scenesPerTopic[numVideo]:
            topic = self.topics[numVideo][topicId]
            for sceneId in sc:
                result.append((sceneId,
                               self.__evaluateScene(numVideo, sceneId, topic)))
            topicId += 1
        sorted_result = sorted(result, key=lambda x:x[1], reverse=True)[:top]
        result = []
        for sceneId, score in sorted_result:
            scene = self.scenes[numVideo][sceneId]
            result.append((scene['start'], scene['end'], scene['text'], score))
        return result

    def __evaluateScene(self, numVideo, sceneId, topic):
        """
        Evalúa la similitd de una escena con la búsqueda del usuario.
        """
        numHits = 0
        score = 0.0
        sceneKeywords = self.scenes[numVideo][sceneId]['keywords']
        for word in self.keywords:
            if word in sceneKeywords:
                numHits += 1
                if word in topic:
                    score += topic[word]
                else:
                    score += 0.001
        return score * numHits

    def __evaluate(self, keywords, topic):
        """
        Evalúa la similitud de de una categoría con la búsqueda del usuario.
        """
        numHits = 0
        score = 0.0
        for word in keywords:
            if word in topic:
                numHits += 1
                score += topic[word]
        return score * numHits
    
    def __evaluateSense(self, word, sense, left):
        """
        Evalúa la probabilidad de que una palabra tenga un sentido determinado
        en el contexto indicado.
        """
        max = 0
        for w, _ in sense:
            if left:
                collation = (word, w)
            else:
                collation = (w, word)
            if collation[0] in self.bigrams:
                value = self.bigrams[collation[0]]
                if collation[1] in value:
                    n = value[collation[1]]
                else:
                    n = 0
            else:
                n = 0
            if n > max:
                max = n
        return max

    def __getBestSense(self, word, senses, left):
        """
        Evalúa los sentidos de una palabra en su contexto. 
        """
        scores = {}
        for i in range(len(senses)):
            label, synonyms = senses[i]
            scores[i] = self.__evaluateSense(word, synonyms, left)
        return scores
    
    def __normalize(self, dic):
        """
        Normaliza los valores contenidos en un diccionario.
        """
        total = 0
        for key in dic:
            total += dic[key]
        if total > 0:
            for key in dic:
                dic[key] /= total

    def __toKey(self, word):
        """
        Pares palabra:tipo
        """
        return word[0] + ':' + word[1]

    def __figureOutSense(self, i, tokens, senses):
        """
        Estima el sentido de una palabra en su contexto.
        """
        score = []
        if i > 0:
            prevToken = tokens[i - 1]
            if prevToken[2] not in ['PUNCT']:
                score.append(self.__getBestSense(prevToken[0], senses, True))
        if i < len(tokens) - 1:
            nextToken = tokens[i + 1]
            if nextToken[2] not in ['PUNCT']:
                score.append(self.__getBestSense(nextToken[0], senses, False))
        if len(score) == 0:
            return -1
        else:
            for dic in score:
                self.__normalize(dic)
            dic = score[0]
            for i in range(1, len(score)):
                for key in dic:
                    dic[key] += score[i][key]
            bestSense = -1
            bestScore = -1
            for key in dic:
                if dic[key] > bestScore:
                    bestScore = dic[key]
                    bestSense = key
            return bestSense

    def __labelVideoSenses(self, tokens):
        """
        Reemplaza una palabra por su sinónimo (atendiendo al sentido de dicha
        palabra en el contexto) ordenado alfabéticamente en primer lugar.
        """
        keywords = []
        for i in range(len(tokens)):
            token = tokens[i]
            key = self.__toKey((token[1], token[2]))
            if token[2] in ['NOUN', 'VERB', 'ADJ', 'PROPN']:
                if key in self.synonyms and token[2] != 'PROPN':
                    value = self.synonyms[key]
                    if len(value) > 0:
                        sense = 0
                        if len(value) > 1:
                            sense = self.__figureOutSense(i, tokens, value)
                        senseSyn = [x for x, _ in value[sense][1]]
                        senseSyn.append(token[1])
                        senseSyn.sort()
                        minSyn = senseSyn[0]
                        key = self.__toKey((minSyn, token[2]))
                keywords.append(key)
        return keywords    
