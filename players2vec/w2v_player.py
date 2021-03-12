import pandas as pd
import numpy as np
import random

import tensorflow.keras.layers as kl
from tensorflow.keras.models import Model

random.seed(123457)

"""
data format(./data/full_player_comparison_final.csv)
name : string
preprocessed : list-like string
"""
# ======================= Preprocessing ==============================


# ========================= Modeling ###############################3
class Players2Vec:
    def __init__(self, df = None):
        self.df = df
        self.info() # 인스턴스 생성과 함께 실행.
        pass

    def to_list(self, x):
        temp = [name.strip()[1:-1] for name in x[1:-1].split(',')]
        return temp

    def make_ngram(self, x, WINDOW_SIZE):
        data = []
        for sentence in x:
            for idx, word in enumerate(sentence):
                for neighbor in sentence[max(idx - WINDOW_SIZE, 0):min(idx + WINDOW_SIZE, len(sentence))]:
                    if neighbor != word:
                        data.append([word, neighbor])
        return data

    def info(self):
        self.df['list'] = self.df['preprocessed'].apply(lambda x: self.to_list(x))
        self.df['string'] = [','.join(map(str, l)) for l in self.df['list']]
        _str = self.df['string'].str.cat(sep=',')
        words = _str.split(',')
        words = list(filter(None, words))
        words = list(set(words))

        self.player_num = len(words)
        self.w2d = {}

        for i, word in enumerate(words):
            self.w2d[word] = i

    def generate_batch(self, pairs = None, n_positive = 50, negative_ratio = 1.0,
                       classification = False):
        """ Generate Batches of samples for training """
        batch_size = n_positive * (1+negative_ratio)
        batch = np.zeros((batch_size, 3))

        # task에 따른 label 조정
        if classification:
            neg_label = 0
        else:
            neg_label = -1

        # generator 생성
        while True:
            for idx, (inp_player, target_player) in enumerate(random.sample(pairs, n_positive)):
                batch[idx, :] = (inp_player, target_player, 1)

            idx+=1

            # add negative examples(총 배치사이즈까지)
            while idx < batch_size:
                random_input = random.randrange(self.player_num)
                random_target = random.randrange(self.player_num)

                # positive example 페이셋에 있는지 확인
                if (random_input, random_target) not in self.pairs_set:
                    batch[idx, :] = (random_input, random_target, neg_label)
                    idx+=1
            np.random.shuffle(batch)
            yield {'input_player':batch[:, 0], 'target_player':batch[:,1]}, batch[:,2]


    def generate_model(self, embed_size = 50, classification = False):
        inp = kl.Input(name = 'input_player', shape=[1])
        target = kl.Input(name = 'target_player', shape=[1])

        # Embedding input player(shape = (None, 1, 50))
        inp_embed = kl.Embedding(name = 'input_embedding',
                                 input_dim = self.player_num,
                                 output_dim = embed_size)(inp)
        # Embedding target player(shape = (None, 1, 50))
        target_embed = kl.Embedding(name = 'target_embedding',
                                    input_dim = self.player_num,
                                    output_dim = embed_size)(target)

        # Merge layers with dot product
        merged = kl.Dot(name = 'dot_product',
                        normalize = True,
                        axes = 2)([inp_embed, target_embed])
        merged = kl.Reshape(target_shape = [1])(merged)

        # If classification
        if classification:
            merged = kl.Dense(1, activation = 'sigmoid')(merged)
            model = Model(inputs = [inp, target], outputs = merged)
            model.compile(optimizer = 'Adam', loss = 'binary_crossentropy',
                          metrics = ['accuracy'])
        else:
            model = Model(inputs = [inp, target], outputs = merged)
            model.compile(optimizer = 'Adam', loss = 'mse')
        return model

    def train(self, n_positive = 256, negative_ratio = 2,
              embed_size = 50, classification = False, epochs = 50, name = None):
        # make pairs by ngram
        data = self.make_ngram(self.df['list'], 3)
        data = pd.DataFrame(data, columns=['input', 'label'])
        data['input'] = data['input'].map(self.w2d)
        data['label'] = data['label'].map(self.w2d)
        pairs = [tuple(x) for x in data[['input', 'label']].to_numpy()]
        self.pairs_set = set(pairs)

        gen = self.generate_batch(pairs=pairs, n_positive = n_positive,
                                  negative_ratio=negative_ratio)
        # train on batch
        model = self.generate_model(embed_size = embed_size, classification=classification)
        print(model.summary())

        hist = model.fit_generator(gen, epochs = epochs,
                                   steps_per_epoch = len(pairs)//n_positive,
                                   verbose = 2,)
        return model, hist

    @staticmethod
    def extract_embeding(model = None, embed_layer_name = None):
        _layer = model.get_layer(embed_layer_name)
        _weights = _layer.get_weights()[0]

        return _weights