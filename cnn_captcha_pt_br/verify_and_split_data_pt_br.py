"""
Verifique o tamanho da imagem e separe o conjunto de teste (5%) e o conjunto de treinamento (95%)
Ele é usado durante a inicialização. Depois que houver uma nova imagem, você pode colocá-la no 
novo diretório e usá-la.
"""
import json
import os
import random
import shutil

from PIL import Image


def verify(origin_dir, real_width, real_height, image_suffix):
    """
    Verifique o tamanho da imagem
    :return:
    """
    if not os.path.exists(origin_dir):
        print("[Aviso] O diretório {} não pode ser encontrado, ele será criado em breve".format(origin_dir))
        os.makedirs(origin_dir)

    print("Comece a verificar a coleção de fotos original")
    # Imagem em tamanho real
    real_size = (real_width, real_height)
    # Lista e quantidade de nomes de fotos
    img_list = os.listdir(origin_dir)
    total_count = len(img_list)
    print("O conjunto original de imagens compartilhadas: {}张".format(total_count))

    # Lista de imagens inválida
    bad_img = []

    # Percorra todas as fotos para verificar
    for index, img_name in enumerate(img_list):
        file_path = os.path.join(origin_dir, img_name)
        # Filtrar imagens com sufixos incorretos
        if not img_name.endswith(image_suffix):
            bad_img.append((index, img_name, "Sufixo de arquivo incorreto"))
            continue

        # Filtrar tags de imagem fora do padrão
        prefix, posfix = img_name.split("_")
        if prefix == "" or posfix == "":
            bad_img.append((index, img_name, "O rótulo da imagem é anormal"))
            continue

        # A imagem não pode ser aberta normalmente
        try:
            img = Image.open(file_path)
        except OSError:
            bad_img.append((index, img_name, "A imagem não pode ser aberta normalmente"))
            continue

        # O tamanho da imagem está anormal
        if real_size == img.size:
            print("{} pass".format(index), end='\r')
        else:
            bad_img.append((index, img_name, "O tamanho da imagem está anormal：{}".format(img.size)))

    print("====As seguintes {} imagens são anormais====".format(len(bad_img)))
    if bad_img:
        for b in bad_img:
            print("[Foto {}] [{}] [{}]".format(b[0], b[1], b[2]))
    else:
        print("Nenhuma anormalidade encontrada（共 {} Fotos）".format(len(img_list)))
    print("========end")
    return bad_img


def split(origin_dir, train_dir, test_dir, bad_imgs):
    """
    Conjunto de treinamento e conjunto de teste separados
    :return:
    """
    if not os.path.exists(origin_dir):
        print("[Aviso] Não é possível encontrar o diretório{}，Prestes a criar".format(origin_dir))
        os.makedirs(origin_dir)

    print("Comece separando a coleção de imagens original como：Conjunto de teste（5%）E conjunto de treinamento（95%）")

    # Lista e quantidade de nomes de fotos
    img_list = os.listdir(origin_dir)
    for img in bad_imgs:
        img_list.remove(img)
    total_count = len(img_list)
    print(
        "Co-distribuição{}Imagens para conjunto de treinamento e conjunto de teste，entre eles{}Zhang Wei foi anormalmente deixado no diretório original".format(
            total_count, len(bad_imgs)))

    # Criar pasta
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)

    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    # Conjunto de teste
    test_count = int(total_count * 0.05)
    test_set = set()
    for i in range(test_count):
        while True:
            file_name = random.choice(img_list)
            if file_name in test_set:
                pass
            else:
                test_set.add(file_name)
                img_list.remove(file_name)
                break

    test_list = list(test_set)
    print("O número de conjuntos de teste é：{}".format(len(test_list)))
    for file_name in test_list:
        src = os.path.join(origin_dir, file_name)
        dst = os.path.join(test_dir, file_name)
        shutil.move(src, dst)

    # Conjunto de treinamento
    train_list = img_list
    print("O número de conjuntos de treinamento é：{}".format(len(train_list)))
    for file_name in train_list:
        src = os.path.join(origin_dir, file_name)
        dst = os.path.join(train_dir, file_name)
        shutil.move(src, dst)

    if os.listdir(origin_dir) == 0:
        print("migration done")


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    # Caminho da imagem
    origin_dir = sample_conf["origin_image_dir"]
    new_dir = sample_conf["new_image_dir"]
    train_dir = sample_conf["train_image_dir"]
    test_dir = sample_conf["test_image_dir"]
    # tamanho da imagem
    real_width = sample_conf["image_width"]
    real_height = sample_conf["image_height"]
    # Sufixo de imagem
    image_suffix = sample_conf["image_suffix"]

    for image_dir in [origin_dir, new_dir]:
        print(">>> Comece a verificar o catálogo：[{}]".format(image_dir))
        bad_images_info = verify(image_dir, real_width, real_height, image_suffix)
        bad_imgs = []
        for info in bad_images_info:
            bad_imgs.append(info[1])
        split(image_dir, train_dir, test_dir, bad_imgs)


if __name__ == '__main__':
    main()
