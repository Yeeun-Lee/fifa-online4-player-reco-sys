from tensorflow.keras.models import load_model
from tensorflow import keras
import numpy as np
import json
from players2vec.w2v_player import Players2Vec

def player_recommend(model, w2d, command):
    player, num = command.split(', ') # ?호날두, 3
    player = player[1:]
    num = int(num)

    player_weights = Players2Vec.extract_embeding(model, 'input_embedding')
    dists = np.dot(player_weights, player_weights[w2d.get(player)].reshape(player_weights.shape))
    sorted_dists = np.argsort(dists)
    closest = sorted_dists[-num-1: len(dists) - 1]

    items=[]
    for c in closest:
        a= [ k for k,v in word2int.items() if v == c ]
        items.append(a)
    return items