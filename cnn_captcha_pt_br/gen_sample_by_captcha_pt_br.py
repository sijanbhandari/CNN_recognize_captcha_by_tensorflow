# -*- coding: UTF-8 -*-
"""
usarcaptcha libGerar código de verificação (pré-requisito：pip install captcha）
"""
import json
import os
import random
import time

from captcha.image import ImageCaptcha


def gen_special_img(text, file_path, width, height):
    # Gerar arquivo img
    generator = ImageCaptcha(width=width, height=height)  # Especifique o tamanho
    img = generator.generate_image(text)  # Gerar imagem
    img.save(file_path)  # Salvar foto


def gen_ima_by_batch(root_dir, image_suffix, characters, count, char_count, width, height):
    # Determine se a pasta existe
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    for index, i in enumerate(range(count)):
        text = ""
        for j in range(char_count):
            text += random.choice(characters)

        timec = str(time.time()).replace(".", "")
        p = os.path.join(root_dir, "{}_{}.{}".format(text, timec, image_suffix))
        gen_special_img(text, p, width, height)

        print("Generate captcha image => {}".format(index + 1))


def main():
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

    gen_ima_by_batch(root_dir, image_suffix, characters, count, char_count, width, height)


if __name__ == '__main__':
    main()
