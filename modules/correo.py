
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Envío de correo electrónico

Descripción:
Permite enviar el contrato de crédito en PDF
mediante el protocolo SMTP.
"""

import os
import ssl
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv


# Cargar las variables de entorno
load_dotenv()


def enviar_contrato(destinatario, nombre, archivo_pdf):
    """
    Envía un contrato PDF por correo electrónico.

    Args:
        destinatario: Correo electrónico del cliente.
        nombre: Nombre del solicitante.
        archivo_pdf: Documento PDF generado en memoria.

    Returns:
        bool: True cuando el servidor SMTP acepta
              el mensaje para su envío.
    """

    # Obtener la configuración del correo
    servidor = os.getenv("SMTP_HOST", "smtp.gmail.com")
    puerto = int(os.getenv("SMTP_PORT", "587"))
    usuario = os.getenv("SMTP_USER")
    contrasena = os.getenv("SMTP_PASSWORD")

    # Verificar que existan las credenciales
    if not usuario or not contrasena:
        raise ValueError(
            "Las credenciales SMTP no están configuradas"
        )

    # Crear el mensaje de correo electrónico
    mensaje = EmailMessage()

    mensaje["Subject"] = "Contrato de crédito"
    mensaje["From"] = usuario
    mensaje["To"] = destinatario

    mensaje.set_content(
        f"Estimado/a {nombre}:\n\n"
        "Adjuntamos el documento correspondiente "
        "a su simulación de crédito.\n\n"
        "Este documento fue generado con fines "
        "académicos.\n\n"
        "Saludos."
    )

    # Adjuntar el contrato PDF
    mensaje.add_attachment(
        archivo_pdf.getvalue(),
        maintype="application",
        subtype="pdf",
        filename="contrato_credito.pdf"
    )

    # Establecer una conexión segura con SMTP
    contexto = ssl.create_default_context()

    with smtplib.SMTP(
        servidor, puerto, timeout=30
    ) as conexion:

        conexion.starttls(context=contexto)
        conexion.login(usuario, contrasena)
        conexion.send_message(mensaje)

    return True
