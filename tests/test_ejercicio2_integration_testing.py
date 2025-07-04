"""
EJERCICIO 2: Integration Testing
Conceptos: Testing de integración entre múltiples componentes
"""

import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.banco import Banco, CuentaNoEncontradaError


class TestIntegracionBanco:
    """Tests de integración entre Banco y Cuenta"""
    
    def test_crear_cuenta_en_banco_y_realizar_operaciones(self):
        """
        GIVEN: Un banco vacío
        WHEN: Se crea una cuenta y se realizan operaciones
        THEN: Todas las operaciones deben funcionar correctamente
        """
        # Given
        banco = Banco("Banco Nacional")
        
        # When - Crear cuenta
        cuenta = banco.crear_cuenta("123456", "María García", 500.0)
        
        # Then - Verificar cuenta creada
        assert cuenta.obtener_saldo() == 500.0
        assert banco.obtener_numero_cuentas() == 1
        
        # When - Realizar operaciones en la cuenta
        cuenta.depositar(200.0)
        cuenta.retirar(100.0)
        
        # Then - Verificar operaciones
        assert cuenta.obtener_saldo() == 600.0
        assert banco.obtener_total_depositado() == 600.0
    
    def test_transferencia_entre_cuentas_exitosa(self):
        """
        GIVEN: Dos cuentas en un banco
        WHEN: Se realiza una transferencia
        THEN: Los saldos deben actualizarse correctamente
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta_origen = banco.crear_cuenta("111111", "Juan Pérez", 1000.0)
        cuenta_destino = banco.crear_cuenta("222222", "Ana López", 500.0)
        
        # When
        resultado = banco.transferir("111111", "222222", 300.0)
        
        # Then
        assert resultado is True
        assert cuenta_origen.obtener_saldo() == 700.0
        assert cuenta_destino.obtener_saldo() == 800.0
        assert banco.obtener_total_depositado() == 1500.0  # Total se mantiene
        assert banco.contador_transacciones == 1
    
    def test_transferencia_con_saldo_insuficiente(self):
        """
        GIVEN: Dos cuentas donde la origen tiene saldo insuficiente
        WHEN: Se intenta realizar una transferencia
        THEN: Debe fallar sin modificar los saldos
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta_origen = banco.crear_cuenta("111111", "Juan Pérez", 100.0)
        cuenta_destino = banco.crear_cuenta("222222", "Ana López", 500.0)
        
        # When/Then
        with pytest.raises(SaldoInsuficienteError):
            banco.transferir("111111", "222222", 200.0)
        
        # Then - Los saldos no deben cambiar
        assert cuenta_origen.obtener_saldo() == 100.0
        assert cuenta_destino.obtener_saldo() == 500.0
        assert banco.contador_transacciones == 0
    
    def test_transferencia_con_cuenta_inexistente(self):
        """
        GIVEN: Un banco con una cuenta
        WHEN: Se intenta transferir a una cuenta inexistente
        THEN: Debe lanzarse CuentaNoEncontradaError
        """
        # Given
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("111111", "Juan Pérez", 1000.0)
        
        # When/Then
        with pytest.raises(CuentaNoEncontradaError):
            banco.transferir("111111", "999999", 100.0)
    
    def test_multiples_operaciones_complejas(self):
        """
        GIVEN: Un banco con múltiples cuentas
        WHEN: Se realizan múltiples operaciones complejas
        THEN: Todos los estados deben mantenerse consistentes
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta1 = banco.crear_cuenta("111111", "Juan Pérez", 1000.0)
        cuenta2 = banco.crear_cuenta("222222", "Ana López", 500.0)
        cuenta3 = banco.crear_cuenta("333333", "Carlos Ruiz", 750.0)
        
        total_inicial = banco.obtener_total_depositado()
        
        # When - Realizar múltiples operaciones
        cuenta1.depositar(200.0)  # 1200
        banco.transferir("111111", "222222", 300.0)  # 900, 800
        cuenta3.retirar(150.0)  # 600
        banco.transferir("222222", "333333", 100.0)  # 700, 700
        
        # Then - Verificar estados finales
        assert cuenta1.obtener_saldo() == 900.0
        assert cuenta2.obtener_saldo() == 700.0
        assert cuenta3.obtener_saldo() == 700.0
        assert banco.obtener_total_depositado() == total_inicial + 200.0 - 150.0  # 2300
        assert banco.contador_transacciones == 2
        
        # Verificar historial de transacciones
        historial1 = cuenta1.obtener_historial()
        historial2 = cuenta2.obtener_historial()
        historial3 = cuenta3.obtener_historial()
        
        assert len(historial1) == 2  # Depósito + retiro (transferencia)
        assert len(historial2) == 2  # Depósito + retiro (transferencias)
        assert len(historial3) == 2  # Retiro + depósito (transferencia)


class TestEjercicioPractico:
    """Tests que los estudiantes deben completar"""
    
    def test_crear_banco_con_multiples_cuentas(self):
        """
        TODO: Completar este test
        GIVEN: Un banco vacío
        WHEN: Se crean múltiples cuentas
        THEN: El banco debe tener el número correcto de cuentas
        """
        # Los estudiantes completan este test
        pass
    
    def test_transferencia_circular_entre_tres_cuentas(self):
        """
        TODO: Completar este test
        GIVEN: Tres cuentas A, B, C con saldos 1000, 500, 300
        WHEN: A transfiere 200 a B, B transfiere 300 a C, C transfiere 100 a A
        THEN: Los saldos finales deben ser A=900, B=400, C=500
        """
        # Los estudiantes completan este test
        pass 
