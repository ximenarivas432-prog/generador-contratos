
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Descripción:
Este archivo contiene la configuración
principal de la aplicación Flask.
"""

import os


class Config:
    """
    Configuración general de la aplicación.

    Attributes:
        SECRET_KEY: Clave utilizada por Flask
                    para funciones de seguridad.
        DEBUG: Activa o desactiva la depuración.
    """

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "clave-temporal-desarrollo"
    )

    DEBUG = False
