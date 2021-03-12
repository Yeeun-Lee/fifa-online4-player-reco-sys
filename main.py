from players2vec.w2v_player import Players2Vec
from players2vec.load_model import player_recommend
import pandas as pd

if __name__=="__main__":
    data = pd.read_csv("data/full_player_comparison_final.csv")
    p2v = Players2Vec(df = data)
    model, hist = p2v.train(n_positive = 50, negative_ratio=2, embed_size=50,
                            epochs = 30)
    command = input("선수 이름과 추천할 개수를 입력하세요(ex. ?호날두, 3) : ")
    out = player_recommend(model, p2v.w2d, command)
    for i, o in enumerate(out):
        print(f"rank {i+1} : {o}")