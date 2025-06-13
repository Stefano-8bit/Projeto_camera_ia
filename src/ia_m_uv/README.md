
# Contador de Pessoas com Alerta por Tempo e E-mail (YOLOv8 + OpenCV)

Este projeto utiliza o modelo YOLOv8 para detecção de pessoas em tempo real com OpenCV, gerando alertas quando:
- O número de pessoas excede um limite configurado.
- Uma pessoa permanece na área monitorada por mais tempo que o permitido.
- Ambos os alertas são registrados em log e enviados por e-mail automaticamente.

## Requisitos

Antes de executar o projeto, você precisa ter:

- Python 3.8 ou superior instalado
- Webcam (para captura em tempo real)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

   Se você ainda não criou o requirements.txt, use:
   ```bash
   pip install ultralytics opencv-python
   ```

## Configurações importantes

- LIMITE_PESSOAS = 1 → define o máximo de pessoas permitidas
- LIMITE_TEMPO_PESSOA = 20 → define o tempo (em segundos) máximo de permanência de uma pessoa

Esses valores podem ser ajustados diretamente no código.

## Configuração de E-mail

Este projeto usa Mailtrap (https://mailtrap.io/) para simulação de envio de e-mails em ambiente de testes.

Altere os seguintes campos no código para seus próprios dados:

```python
SMTP = "sandbox.smtp.mailtrap.io"
PORTA = 587
EMAIL_ORIGEM = "SEU_USUARIO_MAILTRAP"
SENHA_ORIGEM = "SUA_SENHA_MAILTRAP"
EMAIL_CLIENTE = "cliente@teste.com"
```

Você também pode adaptar para Gmail ou outro provedor SMTP real.

## Como executar

Depois de instalar as dependências e configurar o e-mail:

```bash
python main.py
```

Pressione q para encerrar o programa.

## Funcionalidades

- Detecção de pessoas com YOLOv8 em tempo real
- Atribuição de ID único para cada pessoa rastreada
- Verificação de tempo de permanência individual
- Envio de e-mails de alerta
- Registro de alertas em um arquivo log.txt
- Interface com vídeo ao vivo via OpenCV

