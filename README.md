# 🚗🔍 Sistema de Detecção de Placas

Este projeto combina **YOLOv8** e **EasyOCR** para detectar e reconhecer placas de veículos em imagens e em tempo real via webcam.  
Além disso, inclui um conjunto de ferramentas de **processamento de imagens** (histograma, bordas, cores, segmentação, estatísticas) acessíveis por uma interface gráfica feita em **Tkinter**.

---

## 🌟 Funcionalidades

### 🎥 Webcam  
Detecção de placas em tempo real, com OCR integrado.

### 🖼️ Imagem Placa Velha / Nova  
Reconhecimento em imagens pré‑definidas (`carro1.jpg`, `carro2.jpg`).

### 📊 Histograma  
Exibe histograma de intensidade da imagem.

### 🎨 Análise de Cores (HSV)  
Mostra canais de cor e detecta regiões **vermelhas**, **azuis** e **verdes**.

### ✂️ Detecção de Bordas  
Aplica **Canny** para destacar bordas.

### 💡 Brilho / Contraste  
Ajusta parâmetros da imagem e exibe comparação lado a lado.

### 🧩 Segmentação  
Aplica **threshold** simples e adaptativo.

### 📈 Estatísticas da Imagem  
Calcula **média**, **máximo** e **mínimo** de intensidade.

### 🖱️ Interface gráfica  
Botões organizados em um menu para acessar cada funcionalidade.

### 🔠 OCR inteligente  
Valida padrões de placas brasileiras (**antigo** e **Mercosul**).

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Função principal |
|-------------|------------------|
| **OpenCV** | Captura e processamento de imagens/vídeos |
| **Ultralytics YOLOv8** | Modelo de detecção de objetos |
| **EasyOCR** | Reconhecimento óptico de caracteres |
| **Tkinter** | Interface gráfica |
| **Pillow** | Manipulação e exibição de imagens |
| **Matplotlib** | Visualização de histogramas e gráficos |
| **NumPy** | Operações matemáticas e estatísticas |

---

## 📦 Requisitos

Instale as dependências com:

```bash
pip install ultralytics opencv-python easyocr pillow matplotlib numpy
```

> ⚠️ **Observação:** o código roda em **CPU** por padrão, mas terá desempenho muito melhor se você tiver **GPU CUDA** disponível.

---

## ▶️ Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/Augusto-code-dev/De-Yolo-Na-Placa.git
   cd De-Yolo-Na-Placa
   ```
2. Coloque o arquivo do modelo YOLO (`license_plate_detector.pt`) na pasta do projeto.  
3. Execute o programa:
   ```bash
   python main.py
   ```
4. Use os botões da interface para escolher a funcionalidade desejada:
   - 🎥 **Webcam** → abre a câmera e detecta placas em tempo real.  
   - 🖼️ **Imagem Placa Velha / Nova** → roda a detecção em imagens pré‑definidas.  
   - 📊 **Histograma / Bordas / Cores / Brilho / Segmentação / Estatísticas** → ferramentas de análise de imagem.  
   - ❌ **Sair** → fecha o programa.

---

## 📹 Extensão para vídeos

Para rodar em vídeos, basta substituir:

```python
cap = cv2.VideoCapture(0)
```

por:

```python
cap = cv2.VideoCapture("meu_video.mp4")
```

---

## 📚 Créditos

Este projeto utiliza o modelo YOLOv8 para detecção de placas, baseado no trabalho de Muhammad Zeerak Khan [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2FMuhammad-Zeerak-Khan%2FAutomatic-License-Plate-Recognition-using-YOLOv8").  
O OCR foi feito com [EasyOCR](https://github.com/JaidedAI/EasyOCR).  
A interface gráfica e integração com webcam/imagens/vídeos foram adaptadas neste projeto.

---

## 📄 Licença

Distribuído sob a licença **MIT**.
