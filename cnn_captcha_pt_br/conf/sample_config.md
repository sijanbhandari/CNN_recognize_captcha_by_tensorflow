## Pasta de imagens
```
origin_image_dir = "./sample/origin/"  # Arquivo original
train_image_dir = "./sample/train/"   # Conjunto de treinamento
test_image_dir = "./sample/test/"   # Conjunto de teste
api_image_dir = "./sample/api/"   # apiCaminho de armazenamento das fotos recebidas
online_image_dir = "./sample/online/"  # O caminho de armazenamento da imagem obtida do URL do código de verificação
```
## Pasta modelo
```
model_save_dir = "./model/"  # O caminho de armazenamento do modelo treinado
```
## Parâmetros relacionados à imagem
```
image_width = 80  # Largura da imagem
image_height = 40  # Altura da imagem
max_captcha = 4  # Número de caracteres no código de verificação
image_suffix = "jpg"  # Sufixo do arquivo de imagem
```
## Importar tags do arquivo
```
use_labels_json_file = False
```
## Parâmetros relacionados ao caractere do código de verificação
```
char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
char_set = "abcdefghijklmnopqrstuvwxyz"
char_set = "0123456789"
```
## Identificação online do endereço do código de verificação remota
```
remote_url = "http://127.0.0.1:6100/captcha/"
```
## Parâmetros relacionados ao treinamento
```
cycle_stop = 3000  # Pare após o número especificado de iterações
acc_stop = 0.99  # Pare após a taxa de precisão especificada
cycle_save = 500  # Salve uma vez para o número especificado de rodadas de treinamento (sobrescrever o modelo anterior)
enable_gpu = 0  # Para usar GPU ou CPU, você precisa instalar a versão correspondente de tensorflow-gpu == 1.7.0 para usar GPU
```