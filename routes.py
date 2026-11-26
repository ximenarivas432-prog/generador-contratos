
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Rutas y endpoints
Responsable: Integrante 1

Descripción:
Define las rutas que permiten la comunicación
entre el servidor y los demás módulos.
"""

from flask import Blueprint, jsonify, request, render_template, send_file
import math
from amortizacion import calcular_amortizacion
from schemas import SolicitudCredito
from pydantic import ValidationError
from modules.contrato import generar_pdf
from modules.correo import enviar_contrato
import re

# Crear un grupo de rutas
rutas = Blueprint("rutas", __name__)



@rutas.route("/api/estado", methods=["GET"])
def estado():
    """
    Consultar el estado de la API.
    ---
    tags:
      - Estado del sistema
    responses:
      200:
        description: API funcionando correctamente
        examples:
          application/json:
            estado: activo
            mensaje: API funcionando correctamente
    """
    return jsonify({
        "estado": "activo",
        "mensaje": "API funcionando correctamente"
    }), 200


@rutas.route("/api/credito", methods=["POST"])
def recibir_credito():
    
    """
    Recibir y validar los datos básicos del crédito.
    ---
    tags:
      - Créditos
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: credito
        required: true
        schema:
          type: object
          required:
            - monto
            - tasa_anual
            - plazo_meses
          
          properties:
            monto:
              type: number
              minimum: 0.01
              maximum: 100000000
              example: 100000
              description: Monto solicitado del crédito
            tasa_anual:
              type: number
              minimum: 0
              maximum: 100
              example: 12
              description: Tasa nominal anual
            plazo_meses:
              type: integer
              minimum: 1
              maximum: 600
              example: 24
              description: Plazo del crédito en meses

    responses:
      200:
        description: Datos recibidos correctamente
      400:
        description: Datos faltantes o incorrectos
      500:
        description: Error interno del servidor
    """

    # Obtener los datos enviados por el cliente
    datos = request.get_json(silent=True)

    # Verificar que se reciba un objeto JSON
    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON"
        }), 400

    # Definir los campos obligatorios
    campos = ["monto", "tasa_anual", "plazo_meses"]

    # Comprobar que no falte ningún campo
    for campo in campos:
        if campo not in datos:
            return jsonify({
                "error": f"Falta el campo: {campo}"
            }), 400

    # Obtener los valores del crédito
    monto = datos["monto"]
    tasa = datos["tasa_anual"]
    plazo = datos["plazo_meses"]

    
    # Validar que el monto sea numérico, finito y positivo
    if (type(monto) not in (int, float)
            or not math.isfinite(monto)
            or not 0.01 <= monto <= 100000000):
        return jsonify({
            "error": "El monto debe estar entre 0.01 y 100000000"
        }), 400

   
    # Validar que la tasa sea numérica, finita y esté en el rango permitido
    if (type(tasa) not in (int, float)
            or not math.isfinite(tasa)
            or not 0 <= tasa <= 100):
        return jsonify({
            "error": "La tasa debe ser válida y estar entre 0 y 100"
        }), 400

    # Validar que el plazo sea un entero positivo
    if type(plazo) is not int or not 1 <= plazo <= 600:
        return jsonify({
            "error": "El plazo debe estar entre 1 y 600 meses"
        }), 400

    # Confirmar que los datos son válidos
    return jsonify({
        "mensaje": "Datos recibidos correctamente",
        "datos": {
            "monto": monto,
            "tasa_anual": tasa,
            "plazo_meses": plazo
        }
    }), 200

# Manejo de errores HTTP

@rutas.app_errorhandler(404)
def error_no_encontrado(error):
    """
    Maneja las solicitudes a rutas inexistentes.

    Returns:
        JSON: Mensaje de error y código HTTP 404.
    """
    return jsonify({
        "error": "Ruta no encontrada",
        "codigo": 404
    }), 404


@rutas.app_errorhandler(500)
def error_interno(error):
    """
    Maneja errores internos del servidor.

    Returns:
        JSON: Mensaje general y código HTTP 500.
    """
    return jsonify({
        "error": "Error interno del servidor",
        "codigo": 500
    }), 500



@rutas.route("/api/amortizacion", methods=["POST"])
def solicitar_amortizacion():
   
    """
    Calcular la tabla de amortización de un crédito.
    ---
    tags:
      - Amortización
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: credito
        required: true
        schema:
          type: object
          required:
            - monto
            - tasa_anual
            - plazo_meses
          properties:
            monto:
              type: number
              minimum: 0.01
              maximum: 100000000
              example: 100000
            tasa_anual:
              type: number
              minimum: 0
              maximum: 100
              example: 12
            plazo_meses:
              type: integer
              minimum: 1
              maximum: 600
              example: 24

    responses:
      200:
        description: Amortización calculada correctamente
      400:
        description: Datos del crédito incorrectos
      500:
        description: Error interno del servidor
    """

    # Obtener los datos enviados por el cliente
    datos = request.get_json(silent=True)

    # Verificar que los datos sean un objeto JSON
    if not isinstance(datos, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON"
        }), 400

    try:
        # Validar los datos mediante Pydantic
        credito = SolicitudCredito.model_validate(datos)

        # Ejecutar los cálculos financieros
        resultado = calcular_amortizacion(
            credito.monto,
            credito.tasa_anual,
            credito.plazo_meses
        )

        # Devolver los resultados al cliente
        return jsonify({
            "mensaje": "Amortización calculada correctamente",
            "resultado": resultado
        }), 200

    except ValidationError as error:
        # Manejar errores de validación
        return jsonify({
            "error": "Datos del crédito incorrectos",
            "detalles": error.errors(
                include_input=False,
                include_context=False,
                include_url=False
            )
        }), 400

    except ValueError as error:
        # Manejar errores del módulo financiero
        return jsonify({
            "error": str(error)
        }), 400



# Generación de contratos PDF mediante la API

@rutas.route("/api/contrato", methods=["POST"])
def generar_contrato():
    """
    Generar un contrato de crédito en formato PDF.
    ---
    tags:
      - Contratos
    consumes:
      - application/json
    produces:
      - application/pdf
    parameters:
      - in: body
        name: solicitud
        required: true
        schema:
          type: object
          required:
            - nombre
            - monto
            - tasa_anual
            - plazo_meses
          
          properties:
            nombre:
              type: string
              minLength: 1
              maxLength: 120
              example: Cliente de prueba
            monto:
              type: number
              minimum: 0.01
              maximum: 100000000
              example: 100000
            tasa_anual:
              type: number
              minimum: 0
              maximum: 100
              example: 12
            plazo_meses:
              type: integer
              minimum: 1
              maximum: 600
              example: 24
    responses:
      200:
        description: Contrato PDF generado correctamente
        schema:
          type: file
      400:
        description: Datos de la solicitud incorrectos
      500:
        description: Error interno del servidor
    """

    try:
        # Recibir los datos de la solicitud
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            raise ValueError("Se requiere un objeto JSON")

        # Obtener y validar el nombre
        nombre = datos.pop("nombre", "")

        if not isinstance(nombre, str):
            raise ValueError("Nombre incorrecto")

        nombre = nombre.strip()

        if not nombre or len(nombre) > 120:
            raise ValueError("Nombre incorrecto")

        # Validar los datos financieros
        credito = SolicitudCredito.model_validate(datos)

        if not 0.01 <= credito.monto <= 100000000:
            raise ValueError("Monto fuera del rango permitido")

        if not 1 <= credito.plazo_meses <= 600:
            raise ValueError("Plazo fuera del rango permitido")

        # Calcular la tabla de amortización
        resultado = calcular_amortizacion(
            credito.monto,
            credito.tasa_anual,
            credito.plazo_meses
        )

        # Generar el contrato
        archivo = generar_pdf(nombre, resultado)

        # Devolver el documento PDF
        return send_file(
            archivo,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="contrato_credito.pdf"
        )

    except ValidationError as error:
        return jsonify({
            "error": "Datos del crédito incorrectos",
            "detalles": error.errors(
                include_input=False,
                include_context=False,
                include_url=False
            )
        }), 400

    except (ValueError, ArithmeticError) as error:
        return jsonify({
            "error": str(error)
        }), 400


# Manejo de métodos HTTP no permitidos

@rutas.app_errorhandler(405)
def metodo_no_permitido(error):
    """
    Maneja solicitudes que utilizan un método
    HTTP no permitido para una ruta.

    Args:
        error: Excepción generada por Flask.

    Returns:
        JSON: Descripción del error.
        HTTP 405: Método no permitido.
    """
    return jsonify({
        "codigo": 405,
        "error": "Método HTTP no permitido"
    }), 405



@rutas.route("/calcular", methods=["POST"])
def calcular_credito_web():
    """
    Procesa los datos del formulario web.

    Valida la solicitud, realiza los cálculos
    financieros y muestra los resultados
    mediante una plantilla HTML.
    """

    try:
        # Obtener el nombre del solicitante
        nombre = request.form.get("nombre", "").strip()

        if not nombre or len(nombre) > 120:
            raise ValueError("Introduce un nombre válido")

        # Obtener los datos del formulario
        datos = {
            "monto": float(request.form.get("monto", "")),
            "tasa_anual": float(
                request.form.get("tasa_anual", "")
            ),
            "plazo_meses": int(
                request.form.get("plazo_meses", "")
            )
        }

        # Limitar el tamaño de la simulación
        if not 0.01 <= datos["monto"] <= 100000000:
            raise ValueError("Monto fuera del rango permitido")

        if not 1 <= datos["plazo_meses"] <= 600:
            raise ValueError("El plazo debe ser de 1 a 600 meses")

        # Validar los datos con Pydantic
        credito = SolicitudCredito.model_validate(datos)

        # Realizar los cálculos financieros
        resultado = calcular_amortizacion(
            credito.monto,
            credito.tasa_anual,
            credito.plazo_meses
        )

        # Mostrar la página de resultados
        return render_template(
            "resultados.html",
            nombre=nombre,
            resultado=resultado
        )

    except (ValueError, ArithmeticError):
        # Mostrar un mensaje si los datos son incorrectos
        return render_template(
            "index.html",
            error="Verifica los datos de la solicitud."
        ), 400



@rutas.route("/descargar-contrato", methods=["POST"])
def descargar_contrato():
    """
    Genera y descarga el contrato de crédito en PDF.

    Recibe los datos del formulario, valida la
    solicitud y calcula nuevamente la amortización
    antes de generar el documento.

    Returns:
        PDF: Contrato generado para su descarga.
        HTTP 400: Datos incorrectos.
    """

    try:
        # Obtener el nombre del solicitante
        nombre = request.form.get("nombre", "").strip()

        if not nombre or len(nombre) > 120:
            raise ValueError("Nombre incorrecto")

        # Obtener los datos financieros
        datos = {
            "monto": float(request.form.get("monto", "")),
            "tasa_anual": float(
                request.form.get("tasa_anual", "")
            ),
            "plazo_meses": int(
                request.form.get("plazo_meses", "")
            )
        }

        # Verificar los límites permitidos
        if not 0.01 <= datos["monto"] <= 100000000:
            raise ValueError("Monto incorrecto")

        if not 1 <= datos["plazo_meses"] <= 600:
            raise ValueError("Plazo incorrecto")

        # Validar los datos con Pydantic
        credito = SolicitudCredito.model_validate(datos)

        # Calcular la tabla de amortización
        resultado = calcular_amortizacion(
            credito.monto,
            credito.tasa_anual,
            credito.plazo_meses
        )

        # Generar el documento PDF
        archivo = generar_pdf(nombre, resultado)

        # Enviar el archivo al navegador
        return send_file(
            archivo,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="contrato_credito.pdf"
        )

    except (ValueError, ArithmeticError):
        return render_template(
            "index.html",
            error="No fue posible generar el contrato. "
                  "Verifica los datos ingresados."
        ), 400

@rutas.route("/enviar-contrato", methods=["POST"])
def enviar_contrato_web():
    """
    Genera y envía el contrato por correo electrónico.

    Valida los datos del solicitante, comprueba
    el correo del destinatario y genera el PDF
    antes de realizar el envío mediante SMTP.
    """

    try:
        # Obtener los datos del formulario
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()

        # Validar el nombre del solicitante
        if not nombre or len(nombre) > 120:
            raise ValueError("Nombre incorrecto")

        # Comprobar el formato básico del correo
        if len(correo) > 254 or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", correo
        ):
            raise ValueError("Correo electrónico inválido")

        # Obtener los datos financieros
        datos = {
            "monto": float(request.form.get("monto", "")),
            "tasa_anual": float(
                request.form.get("tasa_anual", "")
            ),
            "plazo_meses": int(
                request.form.get("plazo_meses", "")
            )
        }

        # Verificar los límites permitidos
        if not 0.01 <= datos["monto"] <= 100000000:
            raise ValueError("Monto incorrecto")

        if not 1 <= datos["plazo_meses"] <= 600:
            raise ValueError("Plazo incorrecto")

        # Validar los datos con Pydantic
        credito = SolicitudCredito.model_validate(datos)

        # Realizar los cálculos financieros
        resultado = calcular_amortizacion(
            credito.monto,
            credito.tasa_anual,
            credito.plazo_meses
        )

        # Generar el contrato PDF
        archivo = generar_pdf(nombre, resultado)

        # Enviar el documento por correo
        enviar_contrato(correo, nombre, archivo)

        return render_template(
            "resultados.html",
            nombre=nombre,
            resultado=resultado,
            mensaje="Contrato enviado correctamente."
        )

    except (ValueError, ArithmeticError):
        return render_template(
            "index.html",
            error="Verifica los datos o la configuración SMTP."
        ), 400

    except Exception as error:
        print("Tipo de error SMTP:", type(error).__name__)
        print("Codigo SMTP:", getattr(error, "smtp_code", "No disponible"))

        return render_template(
            "index.html",
            error="No fue posible enviar el correo electrónico."
        ), 502