# -*- coding: utf-8 -*-
"""
Identifique a classe de imagem, a fim de identificar rapidamente várias vezes, você pode chamar o seguinte método desta classe：
R = Recognizer(image_height, image_width, max_captcha)
for i in range(10):
    r_img = Image.open(str(i) + ".jpg")
    t = R.rec_image(r_img)
Cada imagem simples pode atingir basicamente a velocidade de reconhecimento de milissegundos
"""
import json

import numpy as np
import tensorflow as tf
from PIL import Image

from cnnlib.network import CNN


class Recognizer(CNN):
    def __init__(self, image_height, image_width, max_captcha, char_set, model_save_dir):
        # Inicializar variáveis
        super(Recognizer, self).__init__(image_height, image_width, max_captcha, char_set, model_save_dir)

        # Novo gráfico e sessão
        self.g = tf.Graph()
        self.sess = tf.Session(graph=self.g)
        # Use o gráfico e a sessão especificados
        with self.g.as_default():
            # Antes de iterar o loop, escreva as expressões de cálculo de todos os tensores usados. Se escrito no loop, ocorrerão vazamentos de memória, 
            # diminuindo a velocidade de reconhecimento
            #  espaço reservado para inicialização tf
            self.X = tf.placeholder(tf.float32, [None, self.image_height * self.image_width])  # 特征向量
            self.Y = tf.placeholder(tf.float32, [None, self.max_captcha * self.char_set_len])  # 标签
            self.keep_prob = tf.placeholder(tf.float32)  # dropout值
            # Carregar parâmetros de rede e modelo
            self.y_predict = self.model()
            self.predict = tf.argmax(tf.reshape(self.y_predict, [-1, self.max_captcha, self.char_set_len]), 2)
            saver = tf.train.Saver()
            with self.sess.as_default() as sess:
                saver.restore(sess, self.model_save_dir)

    # def __del__(self):
    #     self.sess.close()
    #     print("session close")

    def rec_image(self, img):
        # Leia a foto
        img_array = np.array(img)
        test_image = self.convert2gray(img_array)
        test_image = test_image.flatten() / 255
        # Use o gráfico e a sessão especificados
        with self.g.as_default():
            with self.sess.as_default() as sess:
                text_list = sess.run(self.predict, feed_dict={self.X: [test_image], self.keep_prob: 1.})

        # Obter resultados
        predict_text = text_list[0].tolist()
        p_text = ""
        for p in predict_text:
            p_text += str(self.char_set[p])

        # Resultado de reconhecimento de retorno
        return p_text


def main():
    with open("conf/sample_config.json", "r", encoding="utf-8") as f:
        sample_conf = json.load(f)
    image_height = sample_conf["image_height"]
    image_width = sample_conf["image_width"]
    max_captcha = sample_conf["max_captcha"]
    char_set = sample_conf["char_set"]
    model_save_dir = sample_conf["model_save_dir"]
    R = Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)
    r_img = Image.open("./sample/test/2b3n_6915e26c67a52bc0e4e13d216eb62b37.jpg")
    t = R.rec_image(r_img)
    print(t)


if __name__ == '__main__':
    main()
