import numpy as np
import pandas as pd
from numpy.linalg import norm


def cos_sim(A, B):
    return np.dot(A, B)/(norm(A)*norm(B))

def cos_similarity(command):
    player = command[1:].split(", ")[0]
    player1 = command[1:].split(", ")[1]

    data = pd.read_csv("./slack_bot/db/full_stat.csv")
    data = data.fillna(value=0)
    return cos_sim(data.filter(regex = player, axis=0).values[0],
                   data.filter(regex = player1, axis=0).values[0])