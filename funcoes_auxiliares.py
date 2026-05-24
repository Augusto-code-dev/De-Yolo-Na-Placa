import tkinter as tk

BG_COLOR = "#1E1E1E"
CARD_COLOR = "#2A2A2A"
TEXT_COLOR = "white"
PRIMARY = "#91040A"

TITLE_FONT = ("Arial", 18, "bold")
LABEL_FONT = ("Arial", 11, "bold")

#estilo padrao 
btn_style = {
    "font": ("Arial", 12, "bold"),
    "bg": PRIMARY,
    "fg": "white",
    "activebackground": "#B1050D",
    "activeforeground": "white",
    "width": 25,
    "height": 2,
    "bd": 0,
    "cursor": "hand2"
}

def criar_janela(titulo):
    win = tk.Toplevel()
    win.title(titulo)
    win.configure(bg=BG_COLOR)

    titulo_lbl = tk.Label(
        win,
        text=titulo,
        font=TITLE_FONT,
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        pady=15
    )
    titulo_lbl.pack()

    container = tk.Frame(win, bg=BG_COLOR)
    container.pack(padx=15, pady=10)

    return win, container
