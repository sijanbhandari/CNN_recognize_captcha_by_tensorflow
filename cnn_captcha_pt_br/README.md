# cnn_captcha
use CNN recognize captcha by tensorflow.  
Este projeto usa tensorflow para implementar uma rede neural convolucional para códigos de verificação de imagem de caracteres para reconhecimento de código de verificação.
O projeto engloba os módulos mais gerais de ** verificação, treinamento, verificação, reconhecimento e API **, o que reduz muito o tempo e o esforço gastos na identificação de códigos de verificação de caracteres.
  
O projeto ajudou muitos alunos a concluir com eficiência a tarefa de identificação do código de verificação.
Se você tiver um bug e fizer boas melhorias durante o uso, fique à vontade para enviar um problema e uma RP, e o autor responderá o mais rápido possível, na esperança de melhorar o projeto com você.

Se você precisar identificar códigos de verificação de clique, arraste e solte, ou se tiver requisitos de detecção de alvo, você também pode consultar este projeto[nickliqian/darknet_captcha](https://github.com/nickliqian/darknet_captcha)。

# cronograma
#### 2018.11.12
Primeira ediçãoReadme.md  
#### 2018.11.21
Adicione algumas instruções sobre o reconhecimento do código de verificação 
#### 2018.11.24
Otimize as regras para verificar as imagens do conjunto de dados 
#### 2018.11.26
Adicionar`train_model_v2.py`Arquivo, saída da precisão do conjunto de treinamento e conjunto de validação ao mesmo tempo durante o treinamento  
#### 2018.12.06
Recentemente, aumente o suporte de implantação de modelo e conserte váriosbug  
#### 2018.12.08
Otimize a velocidade de reconhecimento do modelo, suporte o teste de estresse da API e as estatísticas demoradas  
#### 2019.02.19
1. Adicionado um novo método de cálculo de taxa de precisão    
2. TAG: v1.0
#### 2019.04.12
1. Mantenha apenas um`train_model.py`Arquivo
2. Otimize a estrutura do código
3. Extraia a configuração geral para`sample_config.json`和`captcha_config.json`
4. Corrija alguns problemas levantados por todos na questão
#### 2019.06.01
1. Melhore o documento leia-me, o documento não é longo, certifique-se de o ler ~
2. Use o diretório cnnlib para armazenar o código da estrutura da rede neural
3.Fizemos uma versão das estatísticas de dados de treinamento, você pode consultar nossos tempos de treinamento, duração e precisão
4. TAG: v2.0  

# índice
<a href="#Project Introdução">1 Introdução ao Projeto</a>  
- <a href="#Sobre o reconhecimento do código de verificação">1.1 Sobre o reconhecimento do código de verificação</a>  
- <a href="#Estrutura de Diretório">1.2Estrutura de Diretório</a>  
- <a href="#confiar">1.3 confiar</a>  
- <a href="#Estrutura do modelo">1.4 Estrutura do modelo</a>  

<a href="#Como usar">2 Como usar</a>  
- <a href="#data set">2.1 conjunto de dados</a>  
- <a href="#Arquivo de configuração">2.2 Arquivo de configuração</a>  
- <a href="#Valide e divida o conjunto de dados">2.3Valide e divida o conjunto de dados</a>  
- <a href="#Modelo de treinamento">2.4Modelo de treinamento</a>  
- <a href="#Bulk Verification">2.5 Verificação de lote</a>  
- <a href="#comeceWebServer">2.6 comeceWebServer</a>  
- <a href="#Identificação da interface de chamada">2.7 Identificação da interface de chamada</a>  
- <a href="#implantar">2.8 implantar</a>  
- <a href="#Implante vários modelos">2.9Implante vários modelos</a>  
- <a href="#Reconhecimento online">2.10 Reconhecimento online</a>  

<a href="#Descrição">3 Dados estatísticos</a>  
- <a href="#Treining data statistics">3.1 Estatísticas de dados de treinamento</a>  
- <a href="#teste de pressão">3.2 teste de pressão</a>  

<a href="#Instruções de desenvolvimento">4 Instruções de desenvolvimento</a>  

<a href="#Um conhecidoBUG">5 Um conhecidoBUG</a>  



# 1 Introdução ao Projeto
## 1.1 Sobre o reconhecimento do código de verificação
O reconhecimento do código de verificação é principalmente um problema encontrado pelos rastreadores e também pode ser usado como um caso introdutório para o reconhecimento de imagem. Atualmente, os seguintes métodos são geralmente usados：  

| Nome do método | Pontos relacionados |
| ------ | ------ |
| tesseract | Adequado apenas para reconhecer imagens sem interferência e distorção，Muito problemático para treinar |
| Outras bibliotecas de reconhecimento de código aberto | Não é geral o suficiente，Taxa de reconhecimento desconhecida |
| PagoOCR API | A situação de alta demanda é muito cara |
| Processamento de imagem + algoritmo de classificação de aprendizado de máquina | Envolvendo uma variedade de tecnologias, altos custos de aprendizagem，E não universal |
| Rede Neural Convolucional | Um certo custo de aprendizagem, o algoritmo é adequado para vários tipos de códigos de verificação |

Aqui, falamos sobre o uso de ** algoritmos de processamento de imagem e aprendizado de máquina ** tradicionais, envolvendo uma variedade de tecnologias:  

1. Processamento de imagem
- Pré-processamento (escala de cinza, binarização)
- Segmentação de imagem
- Recorte (remover borda)
- Filtragem de imagem, redução de ruído
- Vá para o fundo
- Separação de cores
- Rodar
2. Aprendizado de máquina rotativo
- KNN
- SVM

O uso desse tipo de método tem requisitos mais elevados para os usuários e, como existem muitos tipos de mudanças na imagem, o método de processamento não é universal o suficiente e, muitas vezes, leva muito tempo para ajustar as etapas de processamento e algoritmos relacionados.
Usando a ** Rede Neural Convolucional **, você pode realizar o reconhecimento ponta a ponta da maioria dos códigos de verificação de caracteres estáticos com um pré-processamento simples, que é muito eficaz e tem alta versatilidade.

A atual biblioteca de geração de ** código de verificação ** comum está listada aqui：
>referência：[JavaVerificar grupo de família](https://www.cnblogs.com/cynchanpin/p/6912301.html)  

| Língua | Nome da biblioteca de código de verificação | 链接 | Amostra |
| ------ | ------ | ------ | ------ |
| Java | JCaptcha | [Exemplo](https://jcaptcha.atlassian.net/wiki/spaces/general/pages/1212427/Samples+tests)  | ![Efeito 1](./readme_image/jcaptcha1.jpg) ![效果2](./readme_image/jcaptcha2.jpg) ![efeito3](./readme_image/jcaptcha3.jpg) |
| Java | JCaptcha4Struts2 |  |  |
| Java | SimpleCaptcha | [exemplo](https://www.oschina.net/p/simplecaptcha)   | ![效果1](./readme_image/SimpleCaptcha_1.jpg) ![efeito2](./readme_image/SimpleCaptcha_2.jpg) ![效果3](./readme_image/SimpleCaptcha_3.jpg) |
| Java | kaptcha | [exemplo](https://github.com/linghushaoxia/kaptcha) | ![水纹效果](./readme_image/Kaptcha_5.png) ![Efeito Fisheye](./readme_image/Kaptcha_2.png) ![阴影效果](./readme_image/Kaptcha_3.png) |
| Java | patchca |  | ! [Efeito 1](./readme_image/patchca_1.png) |
| Java | imageRandom |  |  |  
| Java | iCaptcha |  | ! [Efeito 1](./readme_image/iCaptcha.jpg) |  
| Java | SkewPassImage |  | ! [Efeito 1](./readme_image/SkewPassImage.jpg) |  
| Java | Cage |  | ! [Efeito 1]](./readme_image/Cage1.jpg) ![效果2](./readme_image/Cage2.jpg) |
| Python | captcha | [exemplo](https://github.com/nickliqian/cnn_captcha/blob/master/gen_image/gen_sample_by_captcha.py) | ![py_Captcha](./readme_image/py_Captcha-1.jpg) |
| Python | pycapt | [exemplo](https://github.com/aboutmydreams/pycapt) | ![pycapt](https://github.com/aboutmydreams/pycapt/raw/master/img/do4.png) |
| PHP | Gregwar/Captcha | [exemplo](https://github.com/Gregwar/Captcha) |  |
| PHP | mewebstudio/captcha | [exemplo](https://github.com/mewebstudio/captcha) |  |

## 1.2 Estrutura de Diretório
### 1.2.1 Configuração básica
| Número de série | nome do arquivo | Descrição |
| ------ | ------ | ------ |
| 1 | `conf/` | Descrição do diretório do arquivo de configuração |
| 2 | `sample/` | Catálogo de conjuntos de dados |
| 3 | `model/` | Diretório do arquivo de modelo |
| 4 | `cnnlib/` | Diretório de código relacionado ao pacote CNN|
### 1.2.2 Modelo de treinamento
| Número de série | nome do arquivo | Descrição |
| ------ | ------ | ------ |
| 1 | verify_and_split_data.py | Conjunto de dados de validação, Divida os dados em conjunto de treinamento e conjunto de teste |
| 2 | network.py | cnnClasse base de rede |
| 3 | train_model.py | Modelo de treinamento |
| 4 | test_batch.py | Verificação de lote |
| 5 | gen_image/gen_sample_by_captcha.py | Script para gerar código de verificação |
| 6 | gen_image/collect_labels.py | Usado para etiquetas de código de verificação estatística (geralmente usado para códigos de verificação chineses) |

### 1.2.3 webinterface
| Número de série | nome do arquivo | Descrição |
| ------ | ------ | ------ |
| 1 | webserver_captcha_image.py | Obtenha a interface do código de verificação |
| 2 | webserver_recognize_api.py | Fornece interface de código de verificação de identificação online |
| 3 | recognize_online.py | Exemplos de uso de reconhecimento de interface |
| 4 | recognize_local.py | Exemplo de teste de imagens locais |
| 5 | recognize_time_test.py | A identificação do teste de estresse é demorada e a resposta da solicitação consome muito tempo |

## 1.3 confiar
```
pip install -r requirements.txt
```
Nota：Se você precisar usar GPU para treinamento，Por favor, coloque no arquivotenforflowmudar paratensorflow-gpu

## 1.4 Estrutura do modelo

| Número de série | Nível do número de série |
| :------: | :------: |
| digitar | input |
| 1 | Camada convolucional + Camada de pooling + Camada de redução da resolução + ReLU  |
| 2 | Camada convolucional + Camada de pooling + Camada de redução da resolução + ReLU  |
| 3 | Camada convolucional + Camada de pooling + Camada de redução da resolução + ReLU  |
| 4 | Totalmente conectado + Camada de redução da resolução + Relu   |
| 5 | Totalmente conectado + softmax  |
| Resultado | output  |

# 2 Como usar
## 2.1 Como usar o conjunto de dados
O conjunto de dados original pode ser armazenado em`./sample/origin`Diretório.  
A fim de facilitar o processamento, a imagem é melhor para`2e8j_17322d3d4226f0b5c5a71d797d2ba7f7.jpg`Nomenclatura do formato (label_serial number. Sufixo).
  
Se você não tem um conjunto de treinamento, você pode usar`gen_sample_by_captcha.py`O arquivo gera o arquivo do conjunto de treinamento.
Você precisa modificar a configuração relevante antes de gerar`conf/captcha_config.json`(Caminho, sufixo do arquivo, conjunto de caracteres, etc.).
```
{
  "root_dir": "sample/origin/",  # Caminho para salvar o código de verificação
  "image_suffix": "png",         # Sufixo da imagem do código de verificação
  "characters": "0123456789",    # Caracteres opcionais para gerar código de verificação
  "count": 1000,                 # O número de fotos que geraram o código de verificação
  "char_count": 4,               # O número de fotos que geraram o código de verificação
  "width": 100,                  # Largura da imagem
  "height": 60                   # Altura da imagem
}
```

## 2.2 Arquivo de configuração
Antes de criar um novo projeto, você precisa ** modificar os arquivos de configuração relacionados ** por conta própria.`conf/sample_config.json`.
```
{
  "origin_image_dir": "sample/origin/",  # Arquivo original
  "new_image_dir": "sample/new_train/",  # Novo exemplo de treinamento
  "train_image_dir": "sample/train/",    # Conjunto de treinamento
  "test_image_dir": "sample/test/",      # Conjunto de teste
  "api_image_dir": "sample/api/",        # apiCaminho de armazenamento das fotos recebidas
  "online_image_dir": "sample/online/",  # O caminho de armazenamento da imagem obtida do URL do código de verificação
  "local_image_dir": "sample/local/",    # Caminho para salvar as fotos localmente
  "model_save_dir": "model/",            # O caminho de armazenamento da imagem obtida do URL do código de verificação
  "image_width": 100,                    # Largura da imagem
  "image_height": 60,                    # Altura da imagem
  "max_captcha": 4,                      # Número de caracteres no código de verificação
  "image_suffix": "png",                 # Sufixo do arquivo de imagem
  "char_set": "0123456789abcdefghijklmnopqrstuvwxyz",  # Categoria de resultado de reconhecimento de código de verificação
  "use_labels_json_file": false,                       # Se deve habilitar a leitura do conteúdo de `labels.json`
  "remote_url": "http://127.0.0.1:6100/captcha/",      # Código de verificação para obter o endereço remotamente
  "cycle_stop": 3000,                                  # O treinamento após o início da tarefa para após o número especificado de vezes
  "acc_stop": 0.99,                                    # Pare após o treinamento com a precisão especificada
  "cycle_save": 500,                                   # Salve o modelo regularmente após o treinamento por um determinado número de vezes
  "enable_gpu": 0,                                     # Se deve habilitar o treinamento GUP
  "train_batch_size": 128,                             # O número de fotos usadas a cada vez durante o treinamento. Se a memória da CPU ou GPU for muito pequena, este parâmetro pode ser reduzido
  "test_batch_size": 100                               # O número de fotos a serem verificadas durante cada lote de testes não deve exceder o número total de conjuntos de códigos de verificação
}

```
Em relação à `categoria de resultado de reconhecimento do código de verificação`, presumindo que sua amostra seja um código de verificação chinês, você pode usar`tools/collect_labels.py`O script executa estatísticas de rótulo.
Irá gerar arquivos`gen_image/labels.json`Armazene todas as tags, definidas no arquivo de configuração`use_labels_json_file = True`Leitura aberta`labels.json`Conteúdo como`Categoria de resultado ».

## 2.3 Valide e divida o conjunto de dados
Esta função irá verificar o tamanho do conjunto de imagens original e se a imagem de teste pode ser aberta, e dividir o conjunto de treinamento e conjunto de teste em uma proporção de 19: 1.
Portanto, você precisa criar e especificar três pastas: origem, treinamento e teste para armazenar os arquivos relacionados.

Você também pode modificá-lo para um diretório diferente, mas é melhor modificá-lo para um caminho absoluto.
Depois que a pasta for criada, execute o seguinte comando：
```
python3 verify_and_split_data.py
```
Geralmente, haverá um prompt semelhante ao seguinte
```
>>> Comece a verificar o catálogo：[sample/origin/]
Comece a verificar a coleção de fotos original
O conjunto original de imagens compartilhadas: 1001Zhang
====A seguinte 1 imagem é anormal====
[Foto 0] [.DStore] [Sufixo de arquivo incorreto]
========end
Comece a separar o conjunto de imagens original: conjunto de teste (5%) e conjunto de treinamento (95%)
Um total de 1000 imagens são alocadas para o conjunto de treinamento e conjunto de teste, uma das quais é uma anomalia e permanece no diretório original
O número de conjuntos de teste é: 50
O número de conjuntos de treinamento é: 950
>>> Comece a verificar o diretório:[sample/new_train/]
Comece a verificar o diretório:sample/new_train/，Prestes a criar
Comece a verificar a coleção de fotos original
O conjunto original de imagens compartilhadas: 0 folhas
====As seguintes 0 imagens são anormais====
Nenhuma anormalidade encontrada (0 fotos no total)
========end
Comece a separar o conjunto de imagens original: conjunto de teste (5%) e conjunto de treinamento (95%)
Um total de 0 imagens são alocadas para o conjunto de treinamento e conjunto de teste, das quais 0 imagens são deixadas no diretório original como anomalias
O número de conjuntos de teste é: 0
O número de conjuntos de treinamento é: 0
```
O programa irá verificar e dividir ao mesmo tempo`origin_image_dir`com`new_image_dir`As fotos nos dois catálogos; haverá mais amostras no futuro, você pode colocar as amostras em`new_image_dir`Execute novamente no diretório`verify_and_split_data`.
O programa deixará arquivos inválidos na pasta original.  

Além disso, quando você tem novas amostras que precisam ser treinadas juntas, você pode colocar`sample/new`Diretório, execute novamente`python3 verify_and_split_data.py`É isso. 
Deve-se notar que se houver novas tags na nova amostra, você precisa adicionar as novas tags a`char_set`É isso. Configurando ou`labels.json`Arquivo. 
 
## 2.4 Modelo de treinamento
Depois de criar o conjunto de treinamento e o conjunto de teste, você pode começar a treinar o modelo. 
Durante o treinamento, um registro será gerado, que mostra o número atual de rodadas de treinamento, precisão e perda.  
** A taxa de precisão neste momento é a taxa de precisão da imagem do conjunto de treinamento, que representa a situação de reconhecimento de imagem do conjunto de treinamento **  
Por exemplo:
```
10º treinamento >>> 
[Conjunto de treinamento] A taxa de precisão do caractere é 0,03000 A taxa de precisão da imagem é 0,00000 >>> loss 0.1698757857
[Conjunto de validação] A taxa de precisão do caractere é 0,04000 A taxa de precisão da imagem é 0,00000 >>> loss 0.1698757857
```
Explicação da precisão do caractere e precisão da imagem：
```
Premissa: Existem 100 imagens, cada imagem tem quatro caracteres, um total de 400 caracteres. Aqui, dividimos a tarefa em 400 caracteres que precisam ser reconhecidos
Precisão do caractere: a porcentagem de caracteres corretos entre os 400 caracteres reconhecidos.
Precisão da imagem: entre 100 imagens, a proporção de imagens com 4 caracteres totalmente reconhecida com precisão.
```
Não vou introduzir especificamente questões relacionadas à instalação do tensorflow aqui, e vou direto ao tópico.
Depois de garantir que os parâmetros relacionados à imagem e as configurações do diretório estão corretos, execute o seguinte comando para iniciar o treinamento:
```
python3 train_model.py
```
Também pode ser baseado em`train_model.py`de`main`O código na função chama a classe para iniciar o treinamento ou realizar uma demonstração de reconhecimento simples.  

Uma vez que o conjunto de treinamento muitas vezes não contém todos os recursos de amostra, haverá casos em que a precisão do conjunto de treinamento é 100% e a precisão do conjunto de teste é inferior a 100%. Neste momento, uma solução para melhorar a precisão é aumentar as amostras negativas após a rotulagem correta.
## 2.5 Verificação de lote
Use as imagens do conjunto de teste para verificar e gerar a taxa de precisão.  
```
python3 test_batch.py
```
O mesmo pode ser baseado em`main`O código na função chama a classe para iniciar a verificação.

## 2.6comeceWebServer
O projeto encapsulou a classe para carregar o modelo e reconhecer a imagem, iniciar`web server`Depois de chamar a interface, o serviço de reconhecimento pode ser usado.  
comece`web server`
```
python3 webserver_recognize_api.py
```
O url da interface é`http://127.0.0.1:6000/b`

## 2.7 Identificação da interface de chamada
usar requestsInterface de chamada:
```
url = "http://127.0.0.1:6000/b"
files = {'image_file': (image_file_name, open('captcha.jpg', 'rb'), 'application')}
r = requests.post(url=url, files=files)
```
O resultado retornado é umjson：
```
{
    'time': '1542017705.9152594',
    'value': 'jsp1',
}
```
Arquivo`recognize_local.py`Este é um exemplo de uso da interface para identificar a área local. Se este exemplo for executado com sucesso, então o processo de identificação do código de verificação está basicamente concluído.  
O código de verificação de identificação online é uma cena comum no display, arquivo`recognize_online.py`É um exemplo de uso da interface para identificação online, consulte:`## 2.11 Reconhecimento online.

## 2.8 implantar
Ao implantar, coloque`webserver_recognize_api.py`Modifique a última linha do arquivo para ler da seguinte forma:
```
app.run(host='0.0.0.0',port=5000,debug=False)
```
Em seguida, abra a autoridade de acesso à porta, você pode acessar através da rede externa.  
Além disso, para habilitar solicitações de processamento de vários processos, você pode usar a combinação uwsgi + nginx para implantação.  
Esta parte pode se referir a:[FlaskOpções de implantação](http://docs.jinkan.org/docs/flask/deploying/index.html)

## 2.9 Implante vários modelos
Implante vários modelos:
no`webserver_recognize_api.py`Resumo do arquivo, crie um novo objeto Reconhecedor; 
E consulte o original`up_image`Lógica de roteamento e identificação escrita pela função.
```
Q = Recognizer(image_height, image_width, max_captcha, char_set, model_save_dir)
```
Preste atenção para modificar esta linha:
```
value = Q.rec_image(img)
```

## 2.10 Reconhecimento online
O código de verificação de identificação online é um cenário comum no display, ou seja, o código de verificação do alvo é obtido em tempo real para chamar a interface de identificação.
Para a integridade do teste, uma interface de aquisição de código de verificação é construída aqui, que é iniciada executando o seguinte comando: 
```
python webserver_captcha_image.py
```
Depois de começar, visitando este endereço：`http://127.0.0.1:6100/captcha/`Você pode receber o arquivo de fluxo binário da imagem do código de verificação.  
Tarefas específicas de identificação onlinedemoVer:`recognize_online.py`。  

# 3 Estatísticas
## 3.1 Estatísticas de dados de treinamento
Muitos alunos fizeram perguntas semelhantes: "Quanto tempo leva para treinar?", "Quanta precisão pode ser alcançada?", "Por que minha precisão é sempre 0?"
Nesta seção, a configuração padrão (2019.06.02) é usada para fazer estatísticas sobre os dados durante o processo de treinamento e para mostrar a todos.
As condições de teste são as seguintes:
-Código de verificação: Este projeto vem com um programa para gerar um código de verificação, números + Inglês minúsculo
-Quantidade: 20.000 folhas
-Motor de computação: GPU
- Modelo GPU: notebook, placa gráfica GTX 950X 2G
  
após o teste:
5000 vezes, 25 minutos, a precisão dos caracteres no conjunto de treinamento é de 84% e a precisão das imagens é de 51%;
9190 vezes, 46 minutos, ** conjunto de treinamento ** a taxa de precisão do caractere é 100%, a taxa de precisão da imagem é 100%;
12.000, 60 minutos, a precisão do ** conjunto de teste ** basicamente não pode ser executada. 

usar`test_batch.py`Teste, o log é o seguinte:  
```
Leva 6,513171672821045 segundos para identificar 100 amostras, com uma taxa de precisão de 37,0%
```
Com uma precisão de 37%, pode-se dizer que é o primeiro passo para uma identificação bem-sucedida.

O gráfico é o seguinte:
Conjunto de treinamento-  
![train_acc](readme_image/train_acc.png) 
   
Conjunto de teste-   
![test_acc](readme_image/test_acc.png)  


## 3.2 Teste de estresse e estatísticas
Fornece um script de teste de estresse simples para estatísticasapiReconhecer e solicitar dados demorados durante o processo em execução, mas o gráfico precisa ser extraído do Excel.  
abrir um arquivo`recognize_time_test.py`，modificar`main`Função sob`test_file`Caminho, aqui irá reutilizar uma imagem para acessar a interface.  
Os dados finais serão armazenados emtest.csvArquivo.
Use o seguinte comando para executar：  
```
python3 recognize_time_test.py
----O resultado é o seguinte
2938,5150,13:30:25,Consome muito tempo：29ms,Identificar：15ms,solicitação：14ms
2939,5150,13:30:25,Consome muito tempo：41ms,Identificar：21ms,solicitação：20ms
2940,5150,13:30:25,Consome muito tempo：47ms,Identificar：16ms,solicitação：31ms
```
Após 20.000 testes em um modelo, um conjunto de dadostest.csv。
Portest.csvApós a análise usando o gráfico de caixa, você pode ver:  
! [Resultado do teste de estresse](readme_image/ Resultados do teste de estresse.png)  
-O tempo total gasto para uma única solicitação de API (média): 27 ms
-Tempo de reconhecimento único (média): 12ms
-Muito demorado por solicitação (média): 15ms
Entre eles estão: tempo total para solicitar API = demorado para identificar + tempo para solicitar  

# 4 Instruções de desenvolvimento
- 20190209  
1. AtualmentetensorboardO suporte da tela não é muito bom.
- 20190601
1. Estive ocupado recentemente，issueÉ um pouco lento，Por favor me perdoe
2. devNo meio do desenvolvimento do branch, não há tempo para obtê-lo，Demorei uma tarde para atualizar sobre o Dia das Crianças hoje:)
3. 感谢看到这里的你，谢谢你的支持

# 4 BUG conhecido
1. usarpycharmIniciar recognize_api.pyErro de arquivo


```
2018-12-01 00:35:15.106333: W T:\src\github\tensorflow\tensorflow\core\framework\op_kernel.cc:1273] OP_REQUIRES failed at save_restore_tensor.cc:170 : Invalid argument: Unsuccessful TensorSliceReader constructor: Failed to get matching files on ./model/: Not found: FindFirstFile failed for: ./model : ϵͳ�Ҳ���ָ����·����
; No such process
......
tensorflow.python.framework.errors_impl.InvalidArgumentError: Unsuccessful TensorSliceReader constructor: Failed to get matching files on ./model/: Not found: FindFirstFile failed for: ./model : ϵͳ\udcd5Ҳ\udcbb\udcb5\udcbdָ\udcb6\udca8\udcb5\udcc4·\udcbe\udcb6\udca1\udca3
; No such process
	 [[Node: save/RestoreV2 = RestoreV2[dtypes=[DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT, DT_FLOAT], _device="/job:localhost/replica:0/task:0/device:CPU:0"](_arg_save/Const_0_0, save/RestoreV2/tensor_names, save/RestoreV2/shape_and_slices)]]
```
A área de trabalho é definida por pycharm por padrão, o que leva a um erro na leitura da pasta de modelo do caminho relativo.
Solução: edite a configuração de execução e defina o espaço de trabalho como o diretório do projeto.
![bug_apifalha ao ativar](readme_image/bug_apifalhou ao ativar.png)

2. FileNotFoundError: [Errno 2] No such file or directory: 'xxxxxx'  
Se houver uma pasta que não existe no diretório, basta criar uma pasta no diretório especificado.

3. apiQuanto mais memória o programa ocupa enquanto está em execução 
Dados de verificação de resultados：[链接](https://blog.csdn.net/The_lastest/article/details/81130500)  
Ao iterar o loop, você não pode mais incluir nenhuma expressão de cálculo de tensor, caso contrário, a memória irá estourar.
Depois que a expressão de cálculo do tensor é colocada na execução de inicialização do init, a velocidade de reconhecimento é muito melhorada.

4. Erro ao carregar vários modelos
O motivo é doisRecognizerTodos os objetos usam o padrãoGraph。
A solução é não usar o padrão ao criar o objetoGraph，Novograph，Então cadaRecognizerTodos usam diferentesgraph，Não haverá conflitos.

5. FlaskPrograma para produção
Você pode consultar os documentos oficiais:[FlaskConfiguração de produção](http://docs.jinkan.org/docs/flask/config.html)

6. OOM happens
```
Hint: If you want to see a list of allocated tensors when OOM happens,
add report_tensor_allocations_upon_oom to RunOptions for current allocation info.
```
Desligue outras tarefas que ocupam GPU ou CPU tanto quanto possível, ou reduza`sample_config.json`meio`train_batch_size`parâmetro.
