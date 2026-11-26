
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Servidor principal
Responsable: Integrante 1

Descripción:
Este archivo crea e inicia la aplicación Flask
y carga la configuración del servidor.
"""

from flask import Flask, render_template
from config import Config
from routes import rutas
from swagger import configurar_swagger

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración
app.config.from_object(Config)
app.register_blueprint(rutas)

# Inicializar la documentación de la API
configurar_swagger(app)

@app.route("/")
def inicio():
    """
    Muestra la página principal del sistema.

    Returns:
        HTML: Formulario de solicitud de crédito.
    """
    return render_template("index.html")


# Ejecutar el servidor
if __name__ == "__main__":
    app.run()
