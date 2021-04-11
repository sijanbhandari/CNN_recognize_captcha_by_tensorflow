#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Use uma interface própria para identificar o código de verificação da rede
Precisa configurar os parâmetros:
remote_url = "https://www.xxxxxxx.com/getImg" endereço do link do código 
de verificação
    rec_times = 1 vez de reconhecimento
"""
import datetime
import json
import os
import time
from io import BytesIO

import requests


def recognize_captcha(test_path, save_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    with open(test_path, "rb") as f:
        content = f.read()

    # Identificar
    s = time.time()
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (image_file_name, BytesIO(content), 'application')}
    r = requests.post(url=url, files=files)
    e = time.time()

    # Resultado de reconhecimento

    print("Resposta da interface: {}".format(r.text))
    predict_text = json.loads(r.text)["value"]
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("【{}】 demorado：{}ms resultado da previsão：{}".format(now_time, int((e - s) * 1000), predict_text))

    # salvar documento
    img_name = "{}_{}.{}".format(predict_text, str(time.time()).replace(".", ""), image_suffix)
    path = os.path.join(save_path, img_name)
    with open(path, "wb") as f:
        f.write(content)
    print("============== end ==============")


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    # Configure os parâmetros relacionados
    test_path = "sample/test/0401_15440848576253345.png"  # Caminho da imagem reconhecido pelo teste
    save_path = sample_conf["local_image_dir"]  # Endereço salvo
    image_suffix = sample_conf["image_suffix"]  # Extensão de arquivo
    recognize_captcha(test_path, save_path, image_suffix)


if __name__ == '__main__':
    main()
