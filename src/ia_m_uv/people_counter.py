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

    desaparecidos = set(tracked_pessoas.keys()) - set(novas_pessoas.keys())
    for pid in desaparecidos:
        if pid in emails_pessoas_enviados:
            del emails_pessoas_enviados[pid]
        del tracked_pessoas[pid]

    total_pessoas = len(novas_pessoas)
    cv2.putText(frame, f"Pessoas detectadas: {total_pessoas}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
    if total_pessoas > LIMITE_PESSOAS:
        alerta = "ALERTA: Limite de pessoas ultrapassado!"
        cv2.putText(frame, alerta, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if not limite_ja_ultrapassado or time.time() - ultimo_alerta > 10:
            print(alerta)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("log.txt", "a") as f:
                f.write(f"[{timestamp}] {alerta}\n")
                for pid in novas_pessoas:
                    tempo = int(time.time() - tracked_pessoas[pid]["tempo"])
                    f.write(f" - Pessoa ID {pid} está na imagem há {tempo} segundos.\n")
                f.write("\n")

            if not email_alerta_enviado:
                corpo = f"O limite de {LIMITE_PESSOAS} pessoas foi ultrapassado.\n"
                corpo += f"Foram detectadas {total_pessoas} pessoas na cena.\n"
                corpo += f"Horário: {timestamp}"
                enviar_email_alerta("⚠️ Alerta: Limite de Pessoas Excedido", corpo)
                email_alerta_enviado = True

            limite_ja_ultrapassado = True
            ultimo_alerta = time.time()
    else:
        limite_ja_ultrapassado = False
        email_alerta_enviado = False

    for pid, (x1, y1, x2, y2) in novas_pessoas.items():
        tempo_na_cena = int(time.time() - tracked_pessoas[pid]["tempo"])
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {pid} - {tempo_na_cena}s", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if tempo_na_cena > LIMITE_TEMPO_PESSOA:
            if pid not in emails_pessoas_enviados:
                corpo = (
                    f"A pessoa ID {pid} está presente na área há {tempo_na_cena} segundos.\n"
                    f"Isso ultrapassa o limite permitido de {LIMITE_TEMPO_PESSOA} segundos.\n"
                    f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                enviar_email_alerta(f"⚠️ Alerta: Pessoa {pid} Excedeu o Tempo", corpo)
                emails_pessoas_enviados[pid] = True



    
                