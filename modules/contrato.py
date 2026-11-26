
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Generación de contratos PDF

Descripción:
Genera un documento PDF con los datos del
solicitante, las condiciones del crédito
y la tabla de amortización.
"""

from io import BytesIO
from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generar_pdf(nombre, resultado):
    """
    Genera un contrato de crédito en formato PDF.

    Args:
        nombre: Nombre del solicitante.
        resultado: Información financiera del crédito.

    Returns:
        BytesIO: Documento PDF generado en memoria.
    """

    # Crear el documento en memoria
    archivo = BytesIO()

    documento = SimpleDocTemplate(
        archivo,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    estilos = getSampleStyleSheet()
    elementos = []

    # Encabezado del documento
    elementos.append(Paragraph(
        "CONTRATO DE CRÉDITO",
        estilos["Title"]
    ))

    elementos.append(Paragraph(
        "Modelo académico de contrato",
        estilos["Normal"]
    ))

    elementos.append(Spacer(1, 15))

    # Datos generales del solicitante
    elementos.append(Paragraph(
        f"Fecha de emisión: {date.today().strftime('%d/%m/%Y')}",
        estilos["Normal"]
    ))

    elementos.append(Paragraph(
        f"Solicitante: {escape(nombre)}",
        estilos["Normal"]
    ))

    elementos.append(Spacer(1, 15))

    # Condiciones financieras
    elementos.append(Paragraph(
        "1. Condiciones del crédito",
        estilos["Heading2"]
    ))

    condiciones = [
        ["Concepto", "Importe o valor"],
        ["Monto del crédito",
         f"${resultado['monto']:,.2f} MXN"],
        ["Tasa nominal anual",
         f"{resultado['tasa_anual']}%"],
        ["Plazo",
         f"{resultado['plazo_meses']} meses"],
        ["Mensualidad ordinaria",
         f"${resultado['mensualidad']:,.2f}"],
        ["Intereses totales",
         f"${resultado['total_intereses']:,.2f}"],
        ["Total a pagar",
         f"${resultado['total_pagado']:,.2f}"]
    ]

    tabla_condiciones = Table(
        condiciones,
        colWidths=[250, 220]
    )

    tabla_condiciones.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#142d4e")),
        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),
        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1),
         0.5, colors.lightgrey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9)
    ]))

    elementos.append(tabla_condiciones)
    elementos.append(Spacer(1, 15))

    # Condiciones de pago
    elementos.append(Paragraph(
        "2. Condiciones de pago",
        estilos["Heading2"]
    ))

    elementos.append(Paragraph(
        "El crédito contempla pagos mensuales vencidos "
        "conforme a la tabla de amortización. Cada pago "
        "incluye los intereses del periodo y la parte "
        "correspondiente al capital. El último pago "
        "puede ajustarse por redondeo.",
        estilos["Normal"]
    ))

    elementos.append(Spacer(1, 15))

    # Tabla de amortización
    elementos.append(Paragraph(
        "3. Tabla de amortización",
        estilos["Heading2"]
    ))

    datos_tabla = [
        ["Mes", "Pago", "Interés", "Capital", "Saldo"]
    ]

    for fila in resultado["tabla"]:
        datos_tabla.append([
            str(fila["periodo"]),
            f"${fila['mensualidad']:,.2f}",
            f"${fila['interes']:,.2f}",
            f"${fila['capital']:,.2f}",
            f"${fila['saldo']:,.2f}"
        ])

    tabla = Table(
        datos_tabla,
        colWidths=[45, 105, 100, 105, 115],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#142d4e")),
        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),
        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1),
         0.5, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#edf3f9")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # Aclaración sobre el uso del documento
    elementos.append(Paragraph(
        "Documento generado con fines académicos. "
        "No constituye por sí mismo un contrato "
        "legalmente vinculante.",
        estilos["Normal"]
    ))

    # Construir el documento PDF
    documento.build(elementos)

    # Regresar al inicio del archivo
    archivo.seek(0)

    return archivo
