Aqui está um **README.md pronto** para você copiar e colar no seu GitHub:

---

# Sistema de Detecção de Placas 🚗🔍

Este projeto utiliza **YOLOv8** e **EasyOCR** para detectar e reconhecer placas de veículos em imagens, vídeos e webcam.  
A interface gráfica foi construída com **Tkinter** para facilitar o uso.

## 🚀 Funcionalidades
- Detecção de placas em **tempo real** via webcam.  
- Reconhecimento de placas em **imagens estáticas**.  
- Possibilidade de rodar em **vídeos gravados** (basta adaptar o `VideoCapture`).  
- Interface gráfica simples com botões para escolher o modo de operação.  

## 🛠️ Tecnologias utilizadas
- [OpenCV](https://opencv.org/) – captura e manipulação de imagens/vídeos.  
- Ultralytics YOLOv8 [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2Fultralytics%2Fultralytics") – modelo de detecção de objetos.  
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) – reconhecimento óptico de caracteres.  
- Tkinter [(docs.python.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fdocs.python.org%2F3%2Flibrary%2Ftkinter.html") – interface gráfica.  
- [Pillow](https://python-pillow.org/) – manipulação de imagens para exibição.  

## 📦 Requisitos
Instale as dependências com:
```bash
pip install ultralytics opencv-python easyocr pillow
```

> ⚠️ Observação: o código roda em **CPU**, mas terá desempenho muito melhor se você tiver **GPU CUDA** disponível.

## ▶️ Como usar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/sistema-deteccao-placas.git
   cd sistema-deteccao-placas
   ```
2. Coloque o arquivo do modelo YOLO (`license_plate_detector.pt`) na pasta do projeto.  
3. Execute o programa:
   ```bash
   python main.py
   ```
4. Use os botões da interface:
   - **Webcam** → abre a câmera e detecta placas em tempo real.  
   - **Imagem Placa Velha / Nova** → roda a detecção em imagens pré-definidas.  
   - **Vídeo** → pode ser adaptado para processar arquivos `.mp4`.  
   - **Sair** → fecha o programa.  

## 📹 Extensão para vídeos
Para rodar em vídeos, basta substituir:
```python
cap = cv2.VideoCapture(0)
```
por:
```python
cap = cv2.VideoCapture("meu_video.mp4")
```

## 📚 Créditos
Este projeto utiliza o modelo YOLOv8 para detecção de placas, baseado no trabalho de Muhammad Zeerak Khan [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2FMuhammad-Zeerak-Khan%2FAutomatic-License-Plate-Recognition-using-YOLOv8").  
O OCR foi feito com [EasyOCR](https://github.com/JaidedAI/EasyOCR).  
A interface gráfica e integração com webcam/imagens/vídeos foram adaptadas neste projeto.

## 📄 Licença
Este projeto é distribuído sob a licença MIT.  

