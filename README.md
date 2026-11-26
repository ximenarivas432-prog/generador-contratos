
# Generador Dinámico de Contratos y Tablas de Amortización

## Descripción del proyecto

El proyecto consiste en una aplicación web desarrollada
en Python mediante Flask, que permite realizar simulaciones
de créditos, calcular mensualidades, generar tablas de
amortización y crear contratos en formato PDF.

También cuenta con un módulo de envío de documentos
por correo electrónico y una API documentada mediante
Swagger.

## Objetivo

Desarrollar una herramienta que facilite la automatización
de cálculos financieros y la generación de documentos
relacionados con solicitudes de crédito.

## Funcionalidades

- Registro de los datos del solicitante.
- Validación de datos mediante Pydantic.
- Cálculo de mensualidades.
- Generación de tablas de amortización.
- Cálculo de intereses y capital amortizado.
- Generación y descarga de contratos PDF.
- Módulo de envío de contratos mediante SMTP.
- Documentación de la API mediante Swagger.
- Manejo de errores HTTP.
- Pruebas unitarias y de integración.

## Tecnologías utilizadas

- Python
- Flask
- Pydantic
- ReportLab
- HTML
- CSS
- Flasgger
- SMTP
- Python-dotenv
- Unittest

## Estructura del proyecto

- app.py: Archivo principal de la aplicación.
- config.py: Configuración del servidor Flask.
- routes.py: Definición de rutas y servicios.
- amortizacion.py: Cálculos financieros.
- schemas.py: Validación de datos.
- swagger.py: Documentación de la API.
- modules/contrato.py: Generación de documentos PDF.
- modules/correo.py: Envío de correo electrónico.
- templates/: Plantillas HTML.
- static/: Archivos de diseño CSS.
- test_amortizacion.py: Pruebas unitarias.
- test_integracion.py: Pruebas de integración.
- requirements.txt: Dependencias del proyecto.
- .env.example: Ejemplo de configuración SMTP.

## Instalación

Abrir una terminal dentro de la carpeta del proyecto
e instalar las dependencias con el siguiente comando:

    python -m pip install -r requirements.txt

## Ejecución

Iniciar el servidor mediante el comando:

    python app.py

Abrir en el navegador:

    http://127.0.0.1:5000/

## Documentación de la API

La documentación interactiva se encuentra en:

    http://127.0.0.1:5000/apidocs/

Rutas disponibles:

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /api/estado | Consultar el estado de la API |
| POST | /api/credito | Validar datos del crédito |
| POST | /api/amortizacion | Calcular la amortización |
| POST | /api/contrato | Generar un contrato PDF |

## Modelo financiero

Se utiliza el sistema de amortización francés, con
mensualidades constantes y pagos al final de cada periodo.

La tasa nominal anual se convierte a una tasa mensual.
Los intereses se calculan sobre el saldo pendiente y
el último pago se ajusta para liquidar el crédito.

Los cálculos no incluyen comisiones ni impuestos.

## Configuración del correo electrónico

Para habilitar el envío mediante SMTP se requiere
configurar las siguientes variables en un archivo .env:

- SMTP_HOST
- SMTP_PORT
- SMTP_USER
- SMTP_PASSWORD

Las credenciales son privadas y no deben compartirse.


El envío de correo electrónico fue comprobado mediante
una prueba simulada y una prueba real utilizando el
servidor SMTP de Gmail.

Se verificó la recepción del correo electrónico
con el contrato PDF adjunto.

## Pruebas

Para ejecutar todas las pruebas automatizadas:

    python -m unittest discover -v

El proyecto cuenta con 7 pruebas unitarias y 9 pruebas
de integración, con un total de 16 pruebas aprobadas
durante su desarrollo.

## Consideraciones

Este proyecto fue desarrollado con fines académicos.
Los contratos generados son modelos de simulación
y no constituyen documentos legales definitivos.
