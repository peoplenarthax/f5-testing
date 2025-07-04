"""
EJERCICIO 1: Unit Testing Básico
Conceptos: Given/When/Then, función vs objeto, testing de caja negra
"""

import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError


class TestCuentaBasico:
    """Tests básicos para la clase Cuenta usando el patrón Given/When/Then"""
    
    def test_crear_cuenta_con_saldo_inicial(self):
        """
        GIVEN: Parámetros válidos para crear una cuenta
        WHEN: Se crea una cuenta con saldo inicial
        THEN: La cuenta debe tener el saldo correcto
        """
        # Given - Datos de entrada
        numero_cuenta = "12345"
        titular = "Juan Pérez"
        saldo_inicial = 1000.0
        
        # When - Acción que probamos
        cuenta = Cuenta(numero_cuenta, titular, saldo_inicial)
        
        # Then - Verificamos el resultado
        assert cuenta.numero_cuenta == numero_cuenta
        assert cuenta.titular == titular
        assert cuenta.obtener_saldo() == saldo_inicial
    
    def test_depositar_dinero_exitosamente(self):
        """
        GIVEN: Una cuenta con saldo inicial
        WHEN: Se deposita dinero
        THEN: El saldo debe aumentar correctamente
        """
        # Given
        cuenta = Cuenta("12345", "Juan Pérez", 100.0)
        cantidad_deposito = 50.0
        saldo_esperado = 150.0
        
        # When
        resultado = cuenta.depositar(cantidad_deposito)
        
        # Then
        assert resultado is True
        assert cuenta.obtener_saldo() == saldo_esperado
    
    def test_retirar_dinero_exitosamente(self):
        """
        GIVEN: Una cuenta con saldo suficiente
        WHEN: Se retira dinero
        THEN: El saldo debe disminuir correctamente
        """
        # Given
        cuenta = Cuenta("12345", "Juan Pérez", 100.0)
        cantidad_retiro = 30.0
        saldo_esperado = 70.0
        
        # When
        resultado = cuenta.retirar(cantidad_retiro)
        
        # Then
        assert resultado is True
        assert cuenta.obtener_saldo() == saldo_esperado
    
    def test_retirar_con_saldo_insuficiente_debe_fallar(self):
        """
        GIVEN: Una cuenta con saldo insuficiente
        WHEN: Se intenta retirar más dinero del disponible
        THEN: Debe lanzarse una excepción SaldoInsuficienteError
        """
        # Given
        cuenta = Cuenta("12345", "Juan Pérez", 50.0)
        cantidad_retiro = 100.0
        
        # When/Then - Verificamos que se lance la excepción
        with pytest.raises(SaldoInsuficienteError):
            cuenta.retirar(cantidad_retiro)
        
        # Then - El saldo no debe cambiar
        assert cuenta.obtener_saldo() == 50.0
    
    def test_depositar_cantidad_negativa_debe_fallar(self):
        """
        GIVEN: Una cuenta válida
        WHEN: Se intenta depositar una cantidad negativa
        THEN: Debe lanzarse una excepción ValueError
        """
        # Given
        cuenta = Cuenta("12345", "Juan Pérez", 100.0)
        
        # When/Then
        with pytest.raises(ValueError, match="La cantidad a depositar debe ser positiva"):
            cuenta.depositar(-10.0)
    
    def test_historial_transacciones_se_registra_correctamente(self):
        """
        GIVEN: Una cuenta recién creada
        WHEN: Se realizan varias transacciones
        THEN: El historial debe registrar todas las transacciones
        """
        # Given
        cuenta = Cuenta("12345", "Juan Pérez", 100.0)
        
        # When
        cuenta.depositar(50.0)
        cuenta.retirar(25.0)
        
        # Then
        historial = cuenta.obtener_historial()
        assert len(historial) == 2
        assert historial[0]["tipo"] == "DEPOSITO"
        assert historial[0]["cantidad"] == 50.0
        assert historial[1]["tipo"] == "RETIRO"
        assert historial[1]["cantidad"] == 25.0


# EJERCICIO PRÁCTICO PARA LOS ESTUDIANTES
class TestEjercicioPractico:
    """Tests que los estudiantes deben completar"""
    
    def test_crear_cuenta_sin_saldo_inicial(self):
        """
        GIVEN: Parámetros sin saldo inicial
        WHEN: Se crea una cuenta
        THEN: La cuenta debe tener saldo 0.0
        """
        # TODO: completar este test
        pass
    
    def test_depositar_cero_debe_fallar(self):
        """
        GIVEN: Una cuenta válida
        WHEN: Se intenta depositar 0.0
        THEN: Debe lanzarse una excepción ValueError
        """
        # TODO: completar este test
        pass 
