
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Documentación de la API

Descripción:
Configura Swagger para consultar y probar
los servicios disponibles en la aplicación.
"""

from flasgger import Swagger


def configurar_swagger(app):
    """
    Inicializa la documentación de la API
    dentro de la aplicación Flask.
    """

    plantilla = {
        "swagger": "2.0",
        "info": {
            "title": "Generador Dinámico de Contratos",
            "description": (
                "API para la simulación de créditos, "
                "tablas de amortización y generación "
                "de contratos PDF."
            ),
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"]
    }

    Swagger(app, template=plantilla)
