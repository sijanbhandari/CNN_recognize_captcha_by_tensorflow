# -*- coding: utf-8 -*-
import json

import tensorflow as tf
import numpy as np
import time
from PIL import Image
import random
import os
from cnnlib.network import CNN
import json
import os
import random
import time

import numpy as np
import tensorflow as tf
from PIL import Image

from cnnlib.network import CNN


class TestError(Exception):


    pass


class TestBatch(CNN):
    def __init__(self, img_path, char_set, model_save_dir, total):
        # Caminho do modelo
        self.model_save_dir = model_save_dir
        # Ordem aleatória dos arquivos
        self.img_path = img_path
        self.img_list = os.listdir(img_path)
        random.seed(time.time())
        random.shuffle(self.img_list)

        # Obtenha informações básicas sobre a largura, altura e comprimento de caracteres da imagem
        label, captcha_array = self.gen_captcha_text_image()

        captcha_shape = captcha_array.shape
        captcha_shape_len = len(captcha_shape)
        if captcha_shape_len == 3:
            image_height, image_width, channel = captcha_shape
            self.channel = channel
        elif captcha_shape_len == 2:
            image_height, image_width = captcha_shape
        else:
            raise TestError("Erro ao converter imagem em matriz，Verifique o formato da imagem")

        # Inicializar variáveis
        super(TestBatch, self).__init__(image_height, image_width, len(label), char_set, model_save_dir)
        self.total = total

        # Impressão de informações relacionadas
        print("-->tamanho da imagem: {} X {}".format(image_height, image_width))
        print("-->Comprimento do código de verificação: {}".format(self.max_captcha))
        print("-->Código de verificação total{}aula {}".format(self.char_set_len, char_set))
        print("-->Use o conjunto de teste como {}".format(img_path))

    def gen_captcha_text_image(self):
        """
        Retorna uma forma de matriz do código de verificação e o rótulo da string correspondente
        :return:tuple (str, numpy.array)
        """
        img_name = random.choice(self.img_list)
        # rótulo
        label = img_name.split("_")[0]
        # Arquivo
        img_file = os.path.join(self.img_path, img_name)
        captcha_image = Image.open(img_file)
        captcha_array = np.array(captcha_image)  # Vetorização

        return label, captcha_array

    def test_batch(self):
        y_predict = self.model()
        total = self.total
        right = 0

        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess, self.model_save_dir)
            s = time.time()
            for i in range(total):
                # test_text, test_image = gen_special_num_image(i)
                test_text, test_image = self.gen_captcha_text_image()  # acaso
                test_image = self.convert2gray(test_image)
                test_image = test_image.flatten() / 255

                predict = tf.argmax(tf.reshape(y_predict, [-1, self.max_captcha, self.char_set_len]), 2)
                text_list = sess.run(predict, feed_dict={self.X: [test_image], self.keep_prob: 1.})
                predict_text = text_list[0].tolist()
                p_text = ""
                for p in predict_text:
                    p_text += str(self.char_set[p])
                print("origin: {} predict: {}".format(test_text, p_text))
                if test_text == p_text:
                    right += 1
                else:
                    pass
            e = time.time()
        rate = str(right / total * 100) + "%"
        print("Resultado dos testes： {}/{}".format(right, total))
        print("{}Identificação de amostra demorada{}segundo，Precisão{}".format(total, e - s, rate))


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    test_image_dir = sample_conf["test_image_dir"]
    model_save_dir = sample_conf["model_save_dir"]

    use_labels_json_file = sample_conf['use_labels_json_file']

    if use_labels_json_file:
        with open("tools/labels.json", "r") as f:
            char_set = f.read().strip()
    else:
        char_set = sample_conf["char_set"]

    total = 100
    tb = TestBatch(test_image_dir, char_set, model_save_dir, total)
    tb.test_batch()


if __name__ == '__main__':
    main()
