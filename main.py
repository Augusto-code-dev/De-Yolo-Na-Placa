import cv2
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import easyocr
import re

# ---------------- CONFIG ----------------
CONF_THRESHOLD = 0.35
running = False
frame_count = 0
ultimo_texto = ""

# Modelo YOLO
model = YOLO("license_plate_detector.pt")

# OCR
reader = easyocr.Reader(
    ['en'],
    gpu=True
)


# ---------------- DETECÇÃO ----------------
def detectar_placa_webcam(img, fazer_ocr=True):
    global ultimo_texto

    results = model.predict(
        img,
        conf=CONF_THRESHOLD,
        imgsz=640,
        verbose=False
    )

    annotated = img.copy()
    textos = []

    boxes = results[0].boxes.xyxy.cpu().numpy()

    for box in boxes:
        x1, y1, x2, y2 = map(int, box)

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(img.shape[1], x2)
        y2 = min(img.shape[0], y2)

        # desenha caixa
        cv2.rectangle(
            annotated,
            (x1, y1),
            (x2, y2),
            (10, 4, 145),
            2
        )

        if fazer_ocr:
            placa_crop = img[y1:y2, x1:x2]

            if placa_crop.size == 0:
                continue

            try:
                # ---------------- PREPROCESSAMENTO ----------------
                gray = cv2.cvtColor(
                    placa_crop,
                    cv2.COLOR_BGR2GRAY
                )

                gray = cv2.GaussianBlur(
                    gray,
                    (3, 3),
                    0
                )

                gray = cv2.equalizeHist(gray)

                _, thresh = cv2.threshold(
                    gray,
                    0,
                    255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

                # OCR
                ocr_result = reader.readtext(
                    thresh,
                    allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )

                if ocr_result:
                    for (_, text, conf) in ocr_result:
                        texto_detectado = text.upper().replace(" ", "")

                        # remove caracteres estranhos
                        texto_detectado = re.sub(
                            r'[^A-Z0-9]',
                            '',
                            texto_detectado
                        )

                        # ignora textos inválidos
                        if texto_detectado in ["BRASIL", "MERCOSUL"]:
                            continue

                        # padrão Mercosul
                        padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'

                        # padrão antigo
                        padrao_antigo = r'^[A-Z]{3}[0-9]{4}$'

                        if (
                            re.match(padrao_mercosul, texto_detectado)
                            or re.match(padrao_antigo, texto_detectado)
                        ):
                            if conf > 0.4:
                                ultimo_texto = texto_detectado
                                textos.append(texto_detectado)
                                break

            except:
                pass

        # mostra texto na tela
        if ultimo_texto:
            label_text = f"Placa: {ultimo_texto}"
        else:
            label_text = "Detectando..."

        cv2.putText(
            annotated,
            label_text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    return annotated, textos


# ---------------- EXIBIR IMAGEM ----------------
def show_image_webcam(img, panel, width=640, height=480):
    img_rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    img_resized = cv2.resize(
        img_rgb,
        (width, height)
    )

    img_pil = Image.fromarray(img_resized)
    img_tk = ImageTk.PhotoImage(image=img_pil)

    panel.imgtk = img_tk
    panel.config(image=img_tk)


# ---------------- WEBCAM ----------------
def start_detection(panel, label, cap):
    global running
    global frame_count
    global ultimo_texto

    if not running:
        return

    ret, frame = cap.read()

    if ret:
        frame_count += 1

        # OCR a cada 10 frames
        fazer_ocr = frame_count % 5 == 0

        annotated, textos = detectar_placa_webcam(
            frame,
            fazer_ocr=fazer_ocr
        )

        show_image_webcam(annotated, panel)

        if ultimo_texto:
            label.config(
                text=f"Última placa: {ultimo_texto}"
            )
        else:
            label.config(
                text="Nenhuma placa detectada"
            )

    root.after(
        15,
        start_detection,
        panel,
        label,
        cap
    )


def stop_detection(cap):
    global running
    running = False
    cap.release()


def open_webcam_window():
    global running
    running = True

    cap = cv2.VideoCapture(0)

    # resolução menor = mais leve
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    webcam_win = tk.Toplevel(root)
    webcam_win.title(
        "Webcam - Detecção de Placas"
    )

    panel = tk.Label(webcam_win)
    panel.pack(
        fill="both",
        expand=True
    )

    label = tk.Label(
        webcam_win,
        text="Placa detectada:",
        bg="lightgray"
    )
    label.pack(pady=10)

    btn_stop = tk.Button(
        webcam_win,
        text="Parar Webcam",
        command=lambda: stop_detection(cap)
    )
    btn_stop.pack(
        side="left",
        padx=10,
        pady=10
    )

    start_detection(
        panel,
        label,
        cap
    )


def detectar_placa_img(img):
    results = model(img, conf=CONF_THRESHOLD)
    textos = []
    boxes = results[0].boxes.xyxy.cpu().numpy()
    annotated = img.copy()

    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        placa_crop = img[y1:y2, x1:x2]
        ocr_result = reader.readtext(placa_crop)

        for (_, text, conf) in ocr_result:
            textos.append(text)

        # retângulo da placa
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (10, 4, 145), 3)

        # label final
        label = f"Placa: {', '.join(textos)}"

        # tamanho do texto
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)

        # posição da caixinha (acima da placa)
        box_x1 = x1
        box_y1 = y1 - h - 10
        box_x2 = x1 + w + 10
        box_y2 = y1

        # fundo preenchido
        cv2.rectangle(annotated, (box_x1, box_y1), (box_x2, box_y2), (10, 4, 145), -1)

        # texto em cima da caixa
        cv2.putText(
            annotated,
            label,
            (box_x1 + 5, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    return annotated, textos


def show_image(img, panel, max_width=800, max_height=600):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # calcula proporção
    w, h = img_pil.size
    scale = min(max_width / w, max_height / h)
    new_size = (int(w * scale), int(h * scale))

    img_resized = img_pil.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(image=img_resized)

    panel.imgtk = img_tk
    panel.config(image=img_tk)


# ---------------- IMAGEM ----------------
def open_image_window(img):

    if img is None:
        print("Imagem não encontrada")
        return

    annotated, textos = detectar_placa_img(img)

    image_win = tk.Toplevel(root)
    image_win.title(
        "Imagem - Detecção de Placas"
    )

    panel = tk.Label(image_win)
    panel.pack(
        fill="both",
        expand=True
    )

    show_image(
        annotated,
        panel
    )

    if textos:
        tk.Label(
            image_win,
            text=f"Placa detectada: {', '.join(textos)}",
            bg="lightgray"
        ).pack(pady=10)
    else:
        tk.Label(
            image_win,
            text="Nenhuma placa lida",
            bg="lightgray"
        ).pack(pady=10)


# ---------------- MENU PRINCIPAL ----------------
root = tk.Tk()
root.title("Sistema de Detecção de Placas")

btn_style = (
    "Arial",
    12,
    "bold"
)

btn_webcam = tk.Button(
    root,
    text="Webcam",
    bg="#91040A",
    fg="white",
    font=btn_style,
    command=open_webcam_window,
    height=2,
    width=20
)
btn_webcam.pack(pady=20)

btn_image_placa_velha = tk.Button(
    root,
    text="Imagem Placa Velha",
    bg="#91040A",
    fg="white",
    font=btn_style,
   command=lambda: open_image_window(cv2.imread("carro2.jpg")),
    height=2,
    width=20
)
btn_image_placa_velha.pack(pady=20)

btn_image_placa_nova = tk.Button(
    root,
    text="Imagem Placa Nova",
    bg="#91040A",
    fg="white",
    font=btn_style,
    command=lambda: open_image_window(cv2.imread("carro1.jpg")),
    height=2,
    width=20
)
btn_image_placa_nova.pack(pady=20)

btn_exit = tk.Button(
    root,
    text="Sair",
    bg="#8D040A",
    fg="white",
    font=btn_style,
    command=root.quit,
    height=2,
    width=20
)
btn_exit.pack(pady=20)

root.mainloop()