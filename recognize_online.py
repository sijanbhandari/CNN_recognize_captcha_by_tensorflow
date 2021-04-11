#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Use uma interface própria para identificar o código de verificação da rede
Precisa configurar parâmetros：
    remote_url = "https://www.xxxxxxx.com/getImg"  Endereço do link do código de verificação
    rec_times = 1  Número de reconhecimentos
"""
import datetime
import requests
from io import BytesIO
import time
import json
import os


def recognize_captcha(remote_url, rec_times, save_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    for index in range(rec_times):
        # solicitação
        while True:
            try:
                response = requests.request("GET", remote_url, headers=headers, timeout=6)
                if response.text:
                    break
                else:
                    print("retry, response.text is empty")
            except Exception as ee:
                print(ee)

        # Identificar
        s = time.time()
        url = "http://127.0.0.1:6000/b"
        files = {'image_file': (image_file_name, BytesIO(response.content), 'application')}
        r = requests.post(url=url, files=files)
        e = time.time()

        # Resultado de reconhecimento
        print("Resposta da interface: {}".format(r.text))
        predict_text = json.loads(r.text)["value"]
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("【{}】 index:{} demorado：{}ms resultado da previsão：{}".format(now_time, index, int((e-s)*1000), predict_text))

        # salvar documento
        img_name = "{}_{}.{}".format(predict_text, str(time.time()).replace(".", ""), image_suffix)
        path = os.path.join(save_path, img_name)
        with open(path, "wb") as f:
            f.write(response.content)
        print("============== end ==============")


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    # Configure os parâmetros relacionados
    save_path = sample_conf["online_image_dir"]  # Baixe o endereço onde a foto está salva
    remote_url = sample_conf["remote_url"]  # Endereço do código de verificação da rede
    image_suffix = sample_conf["image_suffix"]  # Extensão de arquivo
    rec_times = 1
    recognize_captcha(remote_url, rec_times, save_path, image_suffix)


if __name__ == '__main__':
    main()
    

