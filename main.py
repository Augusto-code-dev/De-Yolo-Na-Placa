import tkinter as tk
import cv2

from funcoes_auxiliares import BG_COLOR, btn_style

from funcoes_img import (
    mostrar_histograma,
    analisar_cores,
    detectar_bordas,
    ajustar_brilho_contraste,
    segmentar_img,
    estatisticas_img
)

from funcoes_placa import (
    open_webcam_window,
    open_image_window
)

#Menuzin
root = tk.Tk()
root.title("Sistema de Detecção de Placas")
root.geometry("500x750")
root.configure(bg=BG_COLOR)

titulo = tk.Label(
    root,
    text="Sistema de Detecção de Placas",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg="white",
    pady=20
)
titulo.pack()

frame_botoes = tk.Frame(root, bg=BG_COLOR)
frame_botoes.pack(pady=10)

# Botões
btn_webcam = tk.Button(
    frame_botoes,
    text="Webcam",
    command=open_webcam_window,   
    **btn_style
)
btn_webcam.grid(row=0, column=0, pady=8)

btn_image_placa_velha = tk.Button(
    frame_botoes,
    text="Imagem Placa Velha",
    command=lambda: open_image_window(cv2.imread("carro2.jpg")),
    **btn_style
)
btn_image_placa_velha.grid(row=1, column=0, pady=8)

btn_image_placa_nova = tk.Button(
    frame_botoes,
    text="Imagem Placa Nova",
    command=lambda: open_image_window(cv2.imread("carro1.jpg")),
    **btn_style
)
btn_image_placa_nova.grid(row=2, column=0, pady=8)

btn_histograma = tk.Button(
    frame_botoes,
    text="Histograma",
    command=lambda: mostrar_histograma(cv2.imread("carro3.jpeg")),
    **btn_style
)
btn_histograma.grid(row=3, column=0, pady=8)

btn_hsv = tk.Button(
    frame_botoes,
    text="Análise de Cores",
    command=lambda: analisar_cores(cv2.imread("carro3.jpeg"), root),
    **btn_style
)
btn_hsv.grid(row=4, column=0, pady=8)

btn_bordas = tk.Button(
    frame_botoes,
    text="Detecção de Bordas",
    command=lambda: detectar_bordas(cv2.imread("carro3.jpeg"), root),
    **btn_style
)
btn_bordas.grid(row=5, column=0, pady=8)

btn_brilho_contraste = tk.Button(
    frame_botoes,
    text="Brilho / Contraste",
    command=lambda: ajustar_brilho_contraste(cv2.imread("carro3.jpeg"), root),
    **btn_style
)
btn_brilho_contraste.grid(row=6, column=0, pady=8)

btn_segmentacao = tk.Button(
    frame_botoes,
    text="Segmentação",
    command=lambda: segmentar_img(cv2.imread("carro3.jpeg"), root),
    **btn_style
)
btn_segmentacao.grid(row=7, column=0, pady=8)

btn_estatisticas = tk.Button(
    frame_botoes,
    text="Estatísticas da Imagem",
    command=lambda: estatisticas_img(cv2.imread("carro3.jpeg"), root),
    **btn_style
)
btn_estatisticas.grid(row=8, column=0, pady=8)

btn_exit = tk.Button(
    root,
    text="Sair",
    bg="#5A0005",
    fg="white",
    activebackground="#7A0007",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    command=root.quit,
    width=20,
    height=2,
    bd=0,
    cursor="hand2"
)
btn_exit.pack(pady=20)

root.mainloop()
