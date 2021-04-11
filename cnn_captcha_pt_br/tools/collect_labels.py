# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Conte os rótulos das amostras e grave-os no arquivo labels.json
"""
import os
import json
import json
import os

image_dir = "../sample/origin"
image_list = os.listdir(image_dir)

labels = set()
for img in image_list:
    split_result = img.split("_")
    if len(split_result) == 2:
        label, name = split_result
        if label:
            for word in label:
                labels.add(word)
    else:
        pass

print("Total de tags {} espécies".format(len(labels)))

with open("./labels.json", "w") as f:
    f.write(json.dumps("".join(list(labels)), ensure_ascii=False))

print("Grave a lista de tags no arquivolabels.jsonsucesso")
