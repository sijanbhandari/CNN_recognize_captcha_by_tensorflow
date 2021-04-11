# -*- coding: UTF-8 -*-
"""
Construir serviço de interface de flask
receber files={'image_file': ('captcha.jpg', BytesIO(bytes), 'application')} Código de verificação de identificação de parâmetro
Precisa configurar parâmetros：
    image_height = 40
    image_width = 80
    max_captcha = 4
"""
import json
import os
import time
from io import BytesIO

from PIL import Image
from flask import Flask, request, jsonify, Response

from cnnlib.recognition_object import Recognizer

# Use CPU por padrão
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

with open("conf/sample_config.json", "r") as f:
    sample_conf = json.load(f)
# Parâmetro de configuração
image_height = sample_conf["image_height"]
image_width = sample_conf["image_width"]
max_captcha = sample_conf["max_captcha"]
api_image_dir = sample_conf["api_image_dir"]
model_save_dir = sample_conf["model_save_dir"]
image_suffix = sample_conf["image_suffix"]  # Extensão de arquivo
use_labels_json_file = sample_conf['use_labels_json_file']

if use_labels_json_file:
    with open("tools/labels.json", "r") as f:
        char_set = f.read().strip()
else:
    char_set = sample_conf["char_set"]

# FlaskObjeto
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Gerar objetos de reconhecimento，Precisa configurar parâmetros
R = Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)


# Se você precisar usar vários modelos，Você pode consultar o exemplo original para configurar o roteamento e escrever a lógica
# Q = Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)


def response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/b', methods=['POST'])
def up_image():
    if request.method == 'POST' and request.files.get('image_file'):
        timec = str(time.time()).replace(".", "")
        file = request.files.get('image_file')
        img = file.read()
        img = BytesIO(img)
        img = Image.open(img, mode="r")
        # username = request.form.get("name")
        print("Recebendo tamanho da imagem: {}".format(img.size))
        s = time.time()
        value = R.rec_image(img)
        e = time.time()
        print("Resultado de reconhecimento: {}".format(value))
        # Salvar foto
        print("Salvar foto： {}{}_{}.{}".format(api_image_dir, value, timec, image_suffix))
        file_name = "{}_{}.{}".format(value, timec, image_suffix)
        file_path = os.path.join(api_image_dir + file_name)
        img.save(file_path)
        result = {
            'time': timec,  # Timestamp
            'value': value,  # Resultado previsto
            'speed_time(ms)': int((e - s) * 1000)  # Tempo de reconhecimento
        }
        img.close()
        return jsonify(result)
    else:
        content = json.dumps({"error_code": "1001"})
        resp = response_headers(content)
        return resp


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6000,
        debug=True
    )
