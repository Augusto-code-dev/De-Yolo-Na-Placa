import cv2
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import easyocr

CONF_THRESHOLD = 0.5
running = False

model = YOLO("license_plate_detector.pt")

# OCR
reader = easyocr.Reader(['en'])

def detectar_placa(img):
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

def show_image(img, panel, width=640, height=480):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (width, height))
    img_pil = Image.fromarray(img_resized)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    panel.imgtk = img_tk
    panel.config(image=img_tk)

# Webcam
def start_detection(panel, label, cap):
    global running
    if not running:
        return

    ret, frame = cap.read()
    if ret:
        annotated, textos = detectar_placa(frame)
        show_image(annotated, panel)

        if textos:
            label.config(text=f"Placa detectada: {', '.join(textos)}")
        else:
            label.config(text="Nenhuma placa lida")

    root.after(30, start_detection, panel, label, cap)

def stop_detection(cap):
    global running
    running = False
    cap.release()

def open_webcam_window():
    global running
    running = True
    cap = cv2.VideoCapture(0)

    webcam_win = tk.Toplevel(root)
    webcam_win.title("Webcam - Detecção de Placas")

    panel = tk.Label(webcam_win)
    panel.pack(fill="both", expand=True)

    label = tk.Label(webcam_win, text="Placa detectada: ", bg="lightgray")
    label.pack(pady=10)

    btn_stop = tk.Button(webcam_win, text="Parar Webcam", command=lambda: stop_detection(cap))
    btn_stop.pack(side="left", padx=10, pady=10)

    start_detection(panel, label, cap)

# Imagem
def open_image_window():
    img = cv2.imread('carro.jpg')
    annotated, textos = detectar_placa(img)

    image_win = tk.Toplevel(root)
    image_win.title("Imagem - Detecção de Placas")

    panel = tk.Label(image_win)
    panel.pack(fill="both", expand=True)

    show_image(annotated, panel)

    if textos:
        tk.Label(image_win, text=f"Placa detectada: {', '.join(textos)}", bg="lightgray").pack(pady=10)
    else:
        tk.Label(image_win, text="Nenhuma placa lida", bg="lightgray").pack(pady=10)

# Menu principal
root = tk.Tk()
root.title("Sistema de Detecção de Placas")

btn_style = ("Arial", 12, "bold")

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

btn_image = tk.Button(
    root,
    text="Imagem",
    bg="#91040A",
    fg="white",
    font=btn_style,
    command=open_image_window,
    height=2,
    width=20
)
btn_image.pack(pady=20)

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
