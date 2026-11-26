
"""
Proyecto: Generador Dinámico de Contratos
y Tablas de Amortización

Módulo: Pruebas de integración

Descripción:
Comprueba la comunicación entre Flask,
los cálculos financieros y la generación
de contratos PDF.
"""

import unittest
from unittest.mock import patch
from app import app


class TestIntegracion(unittest.TestCase):

    def setUp(self):
        """Preparar el cliente de pruebas."""
        self.cliente = app.test_client()

        self.datos = {
            "monto": 100000,
            "tasa_anual": 12,
            "plazo_meses": 24
        }

    def test_pagina_principal(self):
        """Comprobar el acceso a la página principal."""
        respuesta = self.cliente.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_estado_api(self):
        """Comprobar el funcionamiento de la API."""
        respuesta = self.cliente.get("/api/estado")
        self.assertEqual(respuesta.status_code, 200)

    def test_credito_valido(self):
        """Comprobar una solicitud de crédito válida."""
        respuesta = self.cliente.post(
            "/api/credito", json=self.datos
        )
        self.assertEqual(respuesta.status_code, 200)

    def test_credito_invalido(self):
        """Comprobar el rechazo de montos negativos."""
        datos = self.datos.copy()
        datos["monto"] = -100000

        respuesta = self.cliente.post(
            "/api/credito", json=datos
        )
        self.assertEqual(respuesta.status_code, 400)

    def test_amortizacion(self):
        """Comprobar los cálculos financieros."""
        respuesta = self.cliente.post(
            "/api/amortizacion", json=self.datos
        )

        self.assertEqual(respuesta.status_code, 200)

        resultado = respuesta.get_json()["resultado"]

        self.assertEqual(len(resultado["tabla"]), 24)
        self.assertAlmostEqual(
            resultado["mensualidad"], 4707.35, places=2
        )
        self.assertEqual(
            resultado["tabla"][-1]["saldo"], 0
        )

    def test_contrato_pdf(self):
        """Comprobar la generación del contrato PDF."""
        datos = self.datos.copy()
        datos["nombre"] = "Cliente de prueba"

        respuesta = self.cliente.post(
            "/api/contrato", json=datos
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.mimetype, "application/pdf"
        )
        self.assertTrue(respuesta.data.startswith(b"%PDF"))

    def test_ruta_inexistente(self):
        """Comprobar el manejo del error 404."""
        respuesta = self.cliente.get("/ruta-inexistente")
        self.assertEqual(respuesta.status_code, 404)

    def test_metodo_no_permitido(self):
        """Comprobar el manejo del error 405."""
        respuesta = self.cliente.get("/api/credito")
        self.assertEqual(respuesta.status_code, 405)

    @patch("routes.enviar_contrato", return_value=True)
    def test_envio_correo(self, envio_simulado):
        """Comprobar el envío simulado del contrato."""
        respuesta = self.cliente.post(
            "/enviar-contrato",
            data={
                "nombre": "Cliente de prueba",
                "correo": "cliente@example.com",
                "monto": "100000",
                "tasa_anual": "12",
                "plazo_meses": "24"
            }
        )

        self.assertEqual(respuesta.status_code, 200)
        envio_simulado.assert_called_once()


if __name__ == "__main__":
    unittest.main()
