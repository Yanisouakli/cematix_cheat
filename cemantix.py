import re
import nltk
import pandas as pd
import gensim
import spacy
import numpy as np
from gensim.models import KeyedVectors
import time
from scipy.spatial.distance import cosine
from gensim.models import KeyedVectors
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wdw
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import os
import wget
import time, urllib.request
import requests
import pandas as pd 
import numpy as np


def init(path):
    
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    return model


    # fenetre=wdw(driver,15).until(ec.element_to_be_clickable((By.ID,"dialog-close")))
    # if fenetre is not None:
    #     fenetre.click()

def get_similar_words(model, target_word):
    if target_word in model:
        # Get the top 10 most similar words
        similar_words = model.most_similar(target_word, topn=15)
        return [word for word, _ in similar_words]
    else:
        return []


def submitWords(words, attempts=0):
    if attempts >= 3:
        return  # Arrête la récursion après 3 tentatives sans mots valides

    time.sleep(5)
    for u in words:
        guess = wdw(driver, 15).until(ec.element_to_be_clickable((By.CLASS_NAME, 'guess')))
        guess.clear()
        guess.send_keys(u)
        wdw(driver, 15).until(ec.element_to_be_clickable((By.CLASS_NAME, "guess-btn"))).click()

    div = wdw(driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, "//tbody[@class='guesses']/tr")))
    
    great_word = div[0].find_elements(By.XPATH, '//td[@class="word close"]')
    target_word = great_word[0].text
    
    # Vérifier si le mot cible apparaît plus de 3 fois dans div[1]
    div1 = div[1].find_elements(By.XPATH, '//td[@class="word close"]')
    count = 0
    for word_element in div1:
        if word_element.text == target_word:
            count += 1

    if count >= 3:
        great_word = div[1].find_elements(By.XPATH, '//td[@class="word close"]')  # Changer la source de great_word
        submitWords(words, attempts + 1)  # Réessaie avec le mot de div[1]
    else:
        new_list = get_similar_words(model, target_word)
        submitWords(new_list)

   
model_path = "frWac_no_postag_no_phrase_700_skip_cut50.bin"
model=init(model_path)
l = ["ecole","chat", "chien", "maison", "voiture", "arbre", "fleur", "eau", "soleil", "ciel", "mer", "montagne", "jour", "nuit", "homme", "femme", "enfant", "ami", "famille", "travail", "amour", "temps", "argent", "bonheur", "santé", "école", "musique", "livre", "film", "nourriture", "boisson", "sport", "voyage", "pays", "ville"]
driver= webdriver.Chrome('chromedriver.exe')

#import le model franvec
driver.get('https://cemantix.certitudes.org/')

wdw(driver,15).until(ec.element_to_be_clickable((By.ID,"dialog-close"))).click()
submitWords(l)