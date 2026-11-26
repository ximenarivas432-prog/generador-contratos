
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Validación de datos

Descripción:
Utiliza Pydantic para verificar que los datos
del crédito sean correctos antes de realizar
los cálculos financieros.
"""

from pydantic import BaseModel, Field, ConfigDict


class SolicitudCredito(BaseModel):
    """
    Modelo de validación de una solicitud de crédito.

    Attributes:
        monto: Cantidad solicitada.
        tasa_anual: Tasa anual en porcentaje.
        plazo_meses: Duración del crédito en meses.
    """

    # Configuración de las validaciones
    model_config = ConfigDict(
        strict=True,
        allow_inf_nan=False,
        extra="forbid"
    )


    # El monto debe estar dentro del rango permitido
    monto: float = Field(ge=0.01, le=100000000)

    # La tasa anual debe estar entre 0 y 100
    tasa_anual: float = Field(ge=0, le=100)

    # El plazo debe estar entre 1 y 600 meses
    plazo_meses: int = Field(ge=1, le=600)
