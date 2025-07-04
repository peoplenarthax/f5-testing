"""
EJERCICIO 3: Mocking, Stubbing y Flaky Tests
Conceptos: Manejo de dependencias externas y comportamiento no determinístico
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.banco import Banco, ServicioExternoError
from src.cuenta import Cuenta
import random


class TestMockingBasico:
    """Tests básicos de mocking y stubbing"""
    
    def test_mock_servicio_externo_exitoso(self):
        """
        GIVEN: Un banco que depende de un servicio externo
        WHEN: Se mockea el servicio para que responda exitosamente
        THEN: La validación debe funcionar correctamente
        """
        # Given
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When - Mockeamos el método del servicio externo
        with patch.object(banco, 'validar_cuenta_con_servicio_externo', return_value=True):
            resultado = banco.validar_cuenta_con_servicio_externo("123456")
        
        # Then
        assert resultado is True
    
    def test_mock_servicio_externo_con_error(self):
        """
        GIVEN: Un banco que depende de un servicio externo
        WHEN: Se mockea el servicio para que falle
        THEN: Debe lanzarse la excepción esperada
        """
        # Given
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When/Then - Mockeamos para que lance una excepción
        with patch.object(banco, 'validar_cuenta_con_servicio_externo', 
                         side_effect=ServicioExternoError("Servicio no disponible")):
            with pytest.raises(ServicioExternoError):
                banco.validar_cuenta_con_servicio_externo("123456")
    
    def test_stub_datetime_para_comportamiento_determinista(self):
        """
        GIVEN: Una cuenta que usa datetime.now()
        WHEN: Se stubea datetime para tener un comportamiento determinístico
        THEN: Las fechas deben ser predecibles
        """
        from datetime import datetime
        
        # Given
        fecha_fija = datetime(2023, 12, 25, 10, 30, 0)
        
        # When - Stubear datetime.now()
        with patch('src.cuenta.datetime') as mock_datetime:
            mock_datetime.now.return_value = fecha_fija
            
            cuenta = Cuenta("123456", "Juan Pérez", 1000.0)
            cuenta.depositar(100.0)
        
        # Then
        assert cuenta.fecha_creacion == fecha_fija
        historial = cuenta.obtener_historial()
        assert historial[0]["fecha"] == fecha_fija
    
    def test_mock_con_multiples_llamadas(self):
        """
        GIVEN: Un servicio que puede ser llamado múltiples veces
        WHEN: Se configura un mock con diferentes respuestas
        THEN: Debe responder según la configuración
        """
        # Given
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When - Configuramos mock para diferentes respuestas
        with patch.object(banco, 'validar_cuenta_con_servicio_externo') as mock_validar:
            mock_validar.side_effect = [True, False, True]  # Diferentes respuestas
            
            resultado1 = banco.validar_cuenta_con_servicio_externo("123456")
            resultado2 = banco.validar_cuenta_con_servicio_externo("123456")
            resultado3 = banco.validar_cuenta_con_servicio_externo("123456")
        
        # Then
        assert resultado1 is True
        assert resultado2 is False
        assert resultado3 is True
        assert mock_validar.call_count == 3


class TestFlakyTests:
    """Tests que muestran y resuelven problemas de flaky tests"""
    
    def test_flaky_test_problema(self):
        """
        DADO: Un test que falla aleatoriamente (FLAKY)
        CUANDO: Se ejecuta múltiples veces
        ENTONCES: Puede fallar o pasar inconsistentemente
        
        NOTA: Este test es intencionalmente flaky para mostrar el problema
        """
        # Este test fallará aproximadamente 10% de las veces
        # random.seed(42)  # Descomenta para hacerlo determinístico
        
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # Esto puede fallar aleatoriamente
        try:
            resultado = banco.validar_cuenta_con_servicio_externo("123456")
            assert resultado is True
        except ServicioExternoError:
            # En un test real, esto sería problemático
            pytest.skip("Test flaky - servicio externo no disponible")
    
    def test_flaky_test_solucion_con_mock(self):
        """
        DADO: Un test que antes era flaky
        CUANDO: Se usa mock para eliminar la aleatoriedad
        ENTONCES: El test debe ser determinístico
        """
        # Given
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When - Eliminamos la aleatoriedad con mock
        with patch.object(banco, 'validar_cuenta_con_servicio_externo', return_value=True):
            resultado = banco.validar_cuenta_con_servicio_externo("123456")
        
        # Then - Ahora es determinístico
        assert resultado is True
    
    def test_flaky_test_solucion_con_seed(self):
        """
        DADO: Un test que usa random
        CUANDO: Se fija la semilla del random
        ENTONCES: El comportamiento es predecible
        """
        # Given - Fijamos la semilla para comportamiento determinístico
        random.seed(42)
        
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When - Mockeamos random para ser determinístico
        with patch('src.banco.random.random', return_value=0.5):  # Mayor que 0.1
            resultado = banco.validar_cuenta_con_servicio_externo("123456")
        
        # Then
        assert resultado is True
    
    def test_retry_pattern_para_servicios_externos(self):
        """
        DADO: Un servicio externo que puede fallar temporalmente
        CUANDO: Se implementa un patrón de retry
        ENTONCES: El test debe ser más robusto
        """
        banco = Banco("Banco Nacional")
        banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # Simulamos un servicio que falla las primeras 2 veces y luego funciona
        with patch.object(banco, 'validar_cuenta_con_servicio_externo') as mock_validar:
            mock_validar.side_effect = [
                ServicioExternoError("Fallo 1"),
                ServicioExternoError("Fallo 2"),
                True  # Éxito en el tercer intento
            ]
            
            # Implementamos retry simple
            intentos = 0
            max_intentos = 3
            
            while intentos < max_intentos:
                try:
                    resultado = banco.validar_cuenta_con_servicio_externo("123456")
                    break
                except ServicioExternoError:
                    intentos += 1
                    if intentos >= max_intentos:
                        raise
            
            assert resultado is True
            assert mock_validar.call_count == 3


class TestMockingAvanzado:
    """Tests avanzados de mocking"""
    
    def test_spy_pattern_verificar_llamadas(self):
        """
        DADO: Un método que queremos monitorear
        CUANDO: Se usa como spy
        ENTONCES: Podemos verificar cómo fue llamado
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta = banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
        
        # When - Usamos spy para monitorear
        with patch.object(cuenta, 'depositar', wraps=cuenta.depositar) as spy_depositar:
            cuenta.depositar(100.0)
            cuenta.depositar(200.0)
        
        # Then - Verificamos las llamadas
        assert spy_depositar.call_count == 2
        spy_depositar.assert_any_call(100.0)
        spy_depositar.assert_any_call(200.0)
    
    def test_mock_con_context_manager(self):
        """
        DADO: Un recurso que debe ser manejado con context manager
        CUANDO: Se mockea el context manager
        ENTONCES: El comportamiento debe ser correcto
        """
        # Simulamos un recurso externo (como una conexión a base de datos)
        mock_conexion = MagicMock()
        mock_conexion.__enter__.return_value = mock_conexion
        mock_conexion.ejecutar_query.return_value = {"saldo": 1000.0}
        
        with patch('builtins.open', mock_conexion):
            with mock_conexion as conn:
                resultado = conn.ejecutar_query("SELECT * FROM cuentas")
        
        assert resultado["saldo"] == 1000.0
        mock_conexion.__enter__.assert_called_once()
        mock_conexion.__exit__.assert_called_once()


class TestEjercicioPractico:
    """Tests que los estudiantes deben completar"""
    
    def test_mock_transferencia_con_validacion_externa(self):
        """
        TODO: Completar este test
        GIVEN: Un banco que valida transferencias con servicio externo
        WHEN: Se mockea el servicio de validación
        THEN: La transferencia debe completarse exitosamente
        """
        # Los estudiantes deben:
        # 1. Crear banco con dos cuentas
        # 2. Mockear validar_cuenta_con_servicio_externo para que retorne True
        # 3. Realizar transferencia
        # 4. Verificar que la transferencia fue exitosa
        pass
    
    def test_solucionar_flaky_test_con_time_sleep(self):
        """
        TODO: Completar este test
        GIVEN: Un método que usa time.sleep() causando lentitud
        WHEN: Se mockea time.sleep
        THEN: El test debe ejecutarse rápidamente
        """
        # Los estudiantes deben:
        # 1. Identificar el problema con time.sleep en validar_cuenta_con_servicio_externo
        # 2. Mockear time.sleep para que no espere realmente
        # 3. Verificar que el test es rápido
        pass 
