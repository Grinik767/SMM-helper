import cv2
import numpy as np
import os
import pickle
import re
from keras.models import load_model


def get_clean_word(word):
    word = re.sub('[^a-zа-я\d#ё-]', '', word, flags=re.IGNORECASE)
    word = word.strip('-')
    return word


def load_image(path):
    return cv2.cvtColor(cv2.resize(cv2.imread(path), (192, 128)), cv2.COLOR_BGR2RGB) / 255


def get_images(chat_id):
    images = []
    for image in os.listdir(f'data/{chat_id}'):
        images.append(load_image(f'data/{chat_id}/{image}'))
    return images


def get_vectors_from_images(images):
    modelImages = load_model('models/images_res.h5')
    pred = list(modelImages.predict(np.array(images)))
    for i in range(10 - len(pred)):
        pred.append(np.array([0] * 49152))
    return np.array([np.array(pred)])


def tokenize_text(text):
    text = [get_clean_word(word) for word in text.split()]
    text_hash = []
    for word in text:
        if word.startswith('#'):
            text_hash.append(word)
    text_hash = np.array([' '.join(text_hash)])
    text = np.array([' '.join(text)])

    with open('models/tokenizer.pickle', mode='rb') as f:
        tokenizer = pickle.load(f)
    WordIndexes = tokenizer.texts_to_sequences(text)
    WordIndexes = tokenizer.sequences_to_matrix(WordIndexes)
    WordIndexesH = tokenizer.texts_to_sequences(text_hash)
    WordIndexesH = tokenizer.sequences_to_matrix(WordIndexesH)
    return WordIndexes, WordIndexesH


def get_vector_from_tokens(token, tokenH):
    modelText = load_model('models/text_res.h5')
    texts = modelText.predict([token, tokenH])
    return texts


def get_result(images, text):
    modelres = load_model('models/result.h5')
    return modelres.predict([text, images])
