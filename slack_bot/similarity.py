import numpy as np
import pandas as pd
from numpy.linalg import norm


def cos_sim(A, B):
    return np.dot(A, B)/(norm(A)*norm(B))

def cos_similarity(player, player1):
    data = pd.read_csv("./slack_bot/db/full_stat.csv")
    data = data.fillna(value=0)
    return cos_sim(data.loc[player].values, data.loc[player1].values)