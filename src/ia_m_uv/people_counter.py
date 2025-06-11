import cv2
import time
from datetime import datetime
from ultralytics import YOLO
import smtplib
from email.message import EmailMessage

SMTP = "sandbox.smtp.mailtrap.io"
PORTA = 587
EMAIL_ORIGEM = "21e2ea49b6fa16"  # Usuário da conta SMTP
SENHA_ORIGEM = "c9b69e944702c3"  # Senha do SMTP
EMAIL_CLIENTE = "cliente@teste.com"  # E-mail de destino (teste)

def enviar_email_alerta(assunto, corpo):
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = "monitoramento@empresa.com"
    msg["To"] = EMAIL_CLIENTE
    msg.set_content(corpo)

    try:
        with smtplib.SMTP(SMTP, PORTA) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ORIGEM, SENHA_ORIGEM)
            smtp.send_message(msg)
            print("[EMAIL] Alerta enviado com sucesso.")
    except Exception as e:
        print(f"[ERRO EMAIL] Falha ao enviar email: {e}")

model = YOLO("yolov8n.pt")            
LIMITE_PESSOAS = 1                    
LIMITE_TEMPO_PESSOA = 20             
DIST_THRESHOLD = 50                  
cap = cv2.VideoCapture(0)            

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

tracked_pessoas = {}
next_id = 0
limite_ja_ultrapassado = False
ultimo_alerta = 0
email_alerta_enviado = False
emails_pessoas_enviados = {}

def get_center(x1, y1, x2, y2):
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640, conf=0.5)[0]
    pessoas_detectadas = [det for det in results.boxes.data.tolist() if int(det[5]) == 0]
    novas_pessoas = {}

    for (x1, y1, x2, y2, score, cls) in pessoas_detectadas:
        cx, cy = get_center(x1, y1, x2, y2)

        id_encontrado = None
        for pid, data in tracked_pessoas.items():
            pcx, pcy = data["centro"]
            if abs(cx - pcx) < DIST_THRESHOLD and abs(cy - pcy) < DIST_THRESHOLD:
                id_encontrado = pid
                break

        if id_encontrado is None:
            id_encontrado = next_id
            next_id += 1
            tracked_pessoas[id_encontrado] = {"tempo": time.time(), "centro": (cx, cy)}
        else:
            tracked_pessoas[id_encontrado]["centro"] = (cx, cy)

        novas_pessoas[id_encontrado] = (x1, y1, x2, y2)

  