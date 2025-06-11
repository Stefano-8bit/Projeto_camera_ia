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
