#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Use uma interface própria para identificar o código de verificação da rede
Precisa configurar parâmetros：
    remote_url = "https://www.xxxxxxx.com/getImg"  Endereço do link do código de verificação
    rec_times = 1  Número de reconhecimentos
"""
import datetime
import json
import time
from io import BytesIO

import requests


def recognize_captcha(index, test_path, save_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    with open(test_path, "rb") as f:
        content = f.read()

    # Identificar
    s = time.time()
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (image_file_name, BytesIO(content), 'application')}
    r = requests.post(url=url, files=files)
    e = time.time()

    # Parâmetros de teste
    result_dict = json.loads(r.text)["value"]  # resposta
    predict_text = result_dict["value"]  # Resultado de reconhecimento
    whole_time_for_work = int((e - s) * 1000)
    speed_time_by_rec = result_dict["speed_time(ms)"]  # O reconhecimento do modelo é demorado
    request_time_by_rec = whole_time_for_work - speed_time_by_rec  # Solicitar demorado
    now_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S')  # hora atual

    # Registro
    log = "{},{},{},{},{},{}\n" \
        .format(index, predict_text, now_time, whole_time_for_work, speed_time_by_rec, request_time_by_rec)
    with open("./test.csv", "a+") as f:
        f.write(log)

    # Resultados de saída para o console
    print("frequência：{},resultado：{},Tempo：{},Consome muito tempo：{}ms,Identificar：{}ms,solicitação：{}ms"
          .format(index, predict_text, now_time, whole_time_for_work, speed_time_by_rec, request_time_by_rec))

    # salvar documento
    # img_name = "{}_{}.{}".format(predict_text, str(time.time()).replace(".", ""), image_suffix)
    # path = os.path.join(save_path, img_name)
    # with open(path, "wb") as f:
    #     f.write(content)


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    # Configure os parâmetros relacionados
    test_file = "sample/test/0001_15430304076164024.png"  # Caminho da imagem reconhecido pelo teste
    save_path = sample_conf["local_image_dir"]  # Endereço salvo
    image_suffix = sample_conf["image_suffix"]  # Extensão de arquivo
    for i in range(20000):
        recognize_captcha(i, test_file, save_path, image_suffix)


if __name__ == '__main__':
    main()
