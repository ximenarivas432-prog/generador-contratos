
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Cálculos financieros

Descripción:
Calcula la mensualidad de un crédito y genera
su tabla de amortización mediante pagos fijos.
"""

from decimal import Decimal, ROUND_HALF_UP


def redondear(valor):
    """Redondea una cantidad monetaria a dos decimales."""
    return valor.quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def calcular_amortizacion(monto, tasa_anual, plazo_meses):
    """
    Calcula la mensualidad y la tabla de amortización.

    Args:
        monto: Cantidad solicitada del crédito.
        tasa_anual: Tasa anual expresada en porcentaje.
        plazo_meses: Número de mensualidades.

    Returns:
        dict: Mensualidad, intereses totales,
              total pagado y tabla de amortización.
    """

    # Convertir los datos para realizar cálculos monetarios
    monto = redondear(Decimal(str(monto)))
    tasa_anual = Decimal(str(tasa_anual))

    # Validar los datos básicos
    if not monto.is_finite() or monto <= 0:
        raise ValueError("El monto debe ser positivo")

    if not tasa_anual.is_finite() or tasa_anual < 0:
        raise ValueError("La tasa debe ser válida")

    if type(plazo_meses) is not int or plazo_meses <= 0:
        raise ValueError("El plazo debe ser un entero positivo")

    # Convertir la tasa anual a mensual
    tasa_mensual = tasa_anual / Decimal("1200")

    # Calcular la mensualidad
    if tasa_mensual == 0:
        mensualidad = monto / plazo_meses
    else:
        mensualidad = (
            monto * tasa_mensual
            / (1 - (1 + tasa_mensual) ** (-plazo_meses))
        )

    mensualidad = redondear(mensualidad)

    # Inicializar las variables
    saldo = monto
    tabla = []
    total_intereses = Decimal("0")
    total_pagado = Decimal("0")

    # Generar la tabla mes por mes
    for periodo in range(1, plazo_meses + 1):

        interes = redondear(saldo * tasa_mensual)
        pago = mensualidad

        # Ajustar el último pago para liquidar el saldo
        if periodo == plazo_meses or pago > saldo + interes:
            pago = saldo + interes

        capital = pago - interes
        saldo = saldo - capital

        total_intereses += interes
        total_pagado += pago

        # Guardar los resultados del periodo
        tabla.append({
            "periodo": periodo,
            "mensualidad": float(pago),
            "interes": float(interes),
            "capital": float(capital),
            "saldo": float(saldo)
        })

    # Devolver los resultados financieros
    return {
        "monto": float(monto),
        "tasa_anual": float(tasa_anual),
        "plazo_meses": plazo_meses,
        "mensualidad": float(mensualidad),
        "total_intereses": float(total_intereses),
        "total_pagado": float(total_pagado),
        "tabla": tabla
    }
