# -*- coding: UTF-8 -*-
"""
    Interface de imagem do código de verificação，访问`/captcha/1`获得图片
"""
import io
import json
import os
import random

from captcha.image import ImageCaptcha
from flask import Flask, request, Response, make_response

# FlaskObjeto
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

with open("conf/captcha_config.json", "r") as f:
    config = json.load(f)
# Parâmetro de configuração
root_dir = config["root_dir"]  # Caminho de armazenamento de imagens
image_suffix = config["image_suffix"]  # Sufixo de armazenamento de imagem
characters = config[
    "characters"]  # Conjunto de caracteres mostrado na imagem # characters = "0123456789abcdefghijklmnopqrstuvwxyz"
count = config["count"]  # Quantas amostras são geradas
char_count = config["char_count"]  # Número de caracteres na imagem

# Definir altura e largura da imagem
width = config["width"]
height = config["height"]


def response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def gen_special_img():
    # Texto aleatório
    text = ""
    for j in range(char_count):
        text += random.choice(characters)
    print(text)
    # Gerar arquivo img
    generator = ImageCaptcha(width=width, height=height)  # Especifique o tamanho
    img = generator.generate_image(text)  # Gerar imagem
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


@app.route('/captcha/', methods=['GET'])
def show_photo():
    if request.method == 'GET':
        image_data = gen_special_img()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        pass


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6100,
        debug=True
    )
