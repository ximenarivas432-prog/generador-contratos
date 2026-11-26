
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Pruebas financieras

Descripción:
Realiza pruebas automáticas para comprobar
los cálculos financieros y las validaciones
de los datos del crédito.
"""

import unittest

from amortizacion import calcular_amortizacion
from schemas import SolicitudCredito
from pydantic import ValidationError


class TestAmortizacion(unittest.TestCase):
    """Pruebas del motor financiero."""

    def test_mensualidad(self):
        """Comprueba el cálculo de la mensualidad."""
        resultado = calcular_amortizacion(100000, 12, 24)

        self.assertAlmostEqual(
            resultado["mensualidad"], 4707.35, places=2
        )

    def test_saldo_final(self):
        """Comprueba que el crédito quede liquidado."""
        resultado = calcular_amortizacion(100000, 12, 24)

        self.assertEqual(
            resultado["tabla"][-1]["saldo"], 0
        )

    def test_numero_periodos(self):
        """Verifica el número de pagos generados."""
        resultado = calcular_amortizacion(100000, 12, 24)

        self.assertEqual(len(resultado["tabla"]), 24)

    def test_tasa_cero(self):
        """Comprueba un crédito sin intereses."""
        resultado = calcular_amortizacion(12000, 0, 12)

        self.assertEqual(resultado["mensualidad"], 1000)
        self.assertEqual(resultado["total_intereses"], 0)

    def test_monto_invalido(self):
        """Comprueba el rechazo de montos negativos."""
        with self.assertRaises(ValidationError):
            SolicitudCredito(
                monto=-5000,
                tasa_anual=12,
                plazo_meses=24
            )

    def test_tasa_invalida(self):
        """Comprueba el rechazo de tasas inválidas."""
        with self.assertRaises(ValidationError):
            SolicitudCredito(
                monto=100000,
                tasa_anual=150,
                plazo_meses=24
            )

    def test_plazo_invalido(self):
        """Comprueba el rechazo de plazos inválidos."""
        with self.assertRaises(ValidationError):
            SolicitudCredito(
                monto=100000,
                tasa_anual=12,
                plazo_meses=0
            )


# Ejecutar las pruebas automáticas
if __name__ == "__main__":
    unittest.main()
