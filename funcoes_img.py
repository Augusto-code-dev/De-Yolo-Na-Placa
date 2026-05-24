import cv2
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import easyocr
import re
import matplotlib.pyplot as plt
import numpy as np

def mostrar_histograma(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    hist = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    )

    img_rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    plt.style.use("dark_background")

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)

    plt.imshow(img_rgb)

    plt.title(
        "Imagem Original",
        fontsize=14
    )

    plt.axis("off")

    plt.subplot(1, 2, 2)

    plt.plot(
        hist,
        color="#ff4d4d",
        linewidth=2
    )

    plt.title(
        "Histograma de Intensidade",
        fontsize=14
    )

    plt.xlabel("Intensidade")
    plt.ylabel("Quantidade de Pixels")

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()

def detectar_bordas(img, root):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    win = tk.Toplevel(root)
    win.title("Detecção de Bordas")
    win.configure(bg="#1E1E1E")

    def show(img, title, row, col):

        if len(img.shape) == 2 or img.shape[2] == 1:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb).resize((250, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        frame = tk.Frame(
            win,
            padx=10,
            pady=10,
            bg="#1E1E1E"
        )
        frame.grid(row=row, column=col)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).pack()

        panel = tk.Label(
            frame,
            image=img_tk,
            bg="#1E1E1E"
        )
        panel.image = img_tk
        panel.pack()

    show(img, "Imagem Original", 0, 0)
    show(edges, "Bordas Detectadas", 0, 1)

def ajustar_brilho_contraste(img, root, alpha=1.2, beta=30):

    ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # cria janela Tkinter
    win = tk.Toplevel(root)
    win.title("Brilho e Contraste")
    win.configure(bg="#1E1E1E")

    def show(img, title, row, col):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb).resize(
            (250, 200),
            Image.LANCZOS
        )

        img_tk = ImageTk.PhotoImage(img_pil)

        frame = tk.Frame(
            win,
            padx=10,
            pady=10,
            bg="#1E1E1E"
        )
        frame.grid(row=row, column=col)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).pack()

        panel = tk.Label(
            frame,
            image=img_tk,
            bg="#1E1E1E"
        )

        panel.image = img_tk
        panel.pack()

    show(img, "Imagem Original", 0, 0)
    show(ajustada, "Imagem Ajustada", 0, 1)

def analisar_cores(img , root):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask_red = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    ) | cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    mask_blue = cv2.inRange(
        hsv,
        lower_blue,
        upper_blue
    )

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    mask_green = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    detect_red = cv2.bitwise_and(img, img, mask=mask_red)
    detect_blue = cv2.bitwise_and(img, img, mask=mask_blue)
    detect_green = cv2.bitwise_and(img, img, mask=mask_green)

    win = tk.Toplevel(root)
    win.title("Análise de Cores")
    win.configure(bg="#1E1E1E")

    def show(img, title, row, col):

        if len(img.shape) == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((250, 200), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_pil)

        frame = tk.Frame(
            win,
            padx=10,
            pady=10,
            bg="#1E1E1E"
        )

        frame.grid(row=row, column=col)

        lbl = tk.Label(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#1E1E1E",
            fg="white"
        )

        lbl.pack()

        panel = tk.Label(
            frame,
            image=img_tk,
            bg="#1E1E1E"
        )

        panel.image = img_tk
        panel.pack()

    show(img, "Original", 0, 0)
    show(h, "Hue", 0, 1)
    show(s, "Saturação", 0, 2)

    show(v, "Valor", 1, 0)
    show(detect_red, "Vermelho Detectado", 1, 1)
    show(detect_blue, "Azul Detectado", 1, 2)

    show(detect_green, "Verde Detectado", 2, 1)

def segmentar_img(img , root):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # simples
    _, thresh = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # adaptativo
    adapt = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    win = tk.Toplevel(root)
    win.title("Segmentação")
    win.configure(bg="#1E1E1E")

    def show(img, title, row, col):

        if len(img.shape) == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb).resize(
            (250, 200),
            Image.LANCZOS
        )

        img_tk = ImageTk.PhotoImage(img_pil)

        frame = tk.Frame(
            win,
            padx=10,
            pady=10,
            bg="#1E1E1E"
        )

        frame.grid(row=row, column=col)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).pack()

        panel = tk.Label(
            frame,
            image=img_tk,
            bg="#1E1E1E"
        )

        panel.image = img_tk
        panel.pack()

    show(img, "Original", 0, 0)
    show(thresh, "Threshold Simples", 0, 1)
    show(adapt, "Threshold Adaptativo", 0, 2)

def estatisticas_img(img, root):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    media_intensidade = np.mean(gray)
    max_intensidade = np.max(gray)
    min_intensidade = np.min(gray)

    # cria janela
    win = tk.Toplevel(root)
    win.title("Estatísticas da Imagem")
    win.configure(bg="#1E1E1E")

    def show(img, title, row, col):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb).resize(
            (250, 200),
            Image.LANCZOS
        )

        img_tk = ImageTk.PhotoImage(img_pil)

        frame = tk.Frame(
            win,
            padx=10,
            pady=10,
            bg="#1E1E1E"
        )

        frame.grid(row=row, column=col)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).pack()

        panel = tk.Label(
            frame,
            image=img_tk,
            bg="#1E1E1E"
        )

        panel.image = img_tk
        panel.pack()

    # imagem original
    show(img, "Imagem Original", 0, 0)

    stats_text = (
        f"Média de intensidade: {media_intensidade:.2f}\n"
        f"Valor máximo: {max_intensidade}\n"
        f"Valor mínimo: {min_intensidade}"
    )

    tk.Label(
        win,
        text=stats_text,
        font=("Arial", 12),
        bg="#1E1E1E",
        fg="white",
        padx=20,
        pady=20,
        justify="left"
    ).grid(row=0, column=1)