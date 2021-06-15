from email.mime.text import MIMEText
import smtplib
# MIME = Multi-Propose Internet Mail Extensions
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv
load_dotenv()

mensaje = MIMEMultipart()
password = environ.get("EMAIL_PASSWORD")
mensaje['From'] = environ.get("EMAIL")
mensaje['Subject'] = "Solicitud de olvido de contraseña"


def enviarCorreo(destinatario, nombre, link):
    """Funcion que sirve para enviar un correo"""
    mensaje['To'] = destinatario
    texto = """Hola {}!
    Has solicitado recuperar tu contraseña. 
    Para tal efececto te enviamos el siguiente link al que deberás ingresar para completar el cambio:
    {}

    Si no fuiste tu, ignora este mensaje.
    """.format(nombre, link)
    mensaje.attach(MIMEText(texto, 'plain'))
    try:
        servidorSMTP = smtplib.SMTP('smtp.gmail.com', 587)
        servidorSMTP.starttls()
        servidorSMTP.login(mensaje['From'], password)
        servidorSMTP.sendmail(
            from_addr=mensaje['From'],
            to_addrs=mensaje['To'],
            msg=mensaje.as_string()
        )
        servidorSMTP.quit()
        return True
    except Exception as error:
        print(error)
        return False
