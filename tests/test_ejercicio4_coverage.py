"""
EJERCICIO 4: Code Coverage
Conceptos: Cobertura de código, líneas cubiertas vs no cubiertas
"""

import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.banco import Banco, CuentaNoEncontradaError


class TestCoverageBasico:
    """Tests para demostrar conceptos básicos de cobertura"""
    
    def test_path_coverage_depositar_exitoso(self):
        """
        Cubre el path exitoso del método depositar
        """
        # Given
        cuenta = Cuenta("123456", "Juan Pérez", 100.0)
        
        # When
        resultado = cuenta.depositar(50.0)
        
        # Then
        assert resultado is True
        assert cuenta.obtener_saldo() == 150.0
    
    def test_path_coverage_depositar_cantidad_negativa(self):
        """
        Cubre el path de error cuando se deposita cantidad negativa
        """
        # Given
        cuenta = Cuenta("123456", "Juan Pérez", 100.0)
        
        # When/Then
        with pytest.raises(ValueError):
            cuenta.depositar(-10.0)
    
    def test_path_coverage_depositar_cantidad_cero(self):
        """
        Cubre el path de error cuando se deposita cero
        """
        # Given
        cuenta = Cuenta("123456", "Juan Pérez", 100.0)
        
        # When/Then
        with pytest.raises(ValueError):
            cuenta.depositar(0.0)
    
    def test_branch_coverage_retirar_todos_los_paths(self):
        """
        Cubre todas las ramas del método retirar
        """
        # Given
        cuenta = Cuenta("123456", "Juan Pérez", 100.0)
        
        # Rama 1: Retiro exitoso
        resultado1 = cuenta.retirar(30.0)
        assert resultado1 is True
        assert cuenta.obtener_saldo() == 70.0
        
        # Rama 2: Cantidad negativa
        with pytest.raises(ValueError):
            cuenta.retirar(-10.0)
        
        # Rama 3: Cantidad cero
        with pytest.raises(ValueError):
            cuenta.retirar(0.0)
        
        # Rama 4: Saldo insuficiente
        with pytest.raises(SaldoInsuficienteError):
            cuenta.retirar(100.0)  # Solo tiene 70.0
    
    def test_line_coverage_metodos_privados(self):
        """
        Asegura que los métodos privados también sean cubiertos
        """
        # Given
        cuenta = Cuenta("123456", "Juan Pérez", 100.0)
        
        # When - Esto llamará al método privado _registrar_transaccion
        cuenta.depositar(50.0)
        cuenta.retirar(25.0)
        
        # Then - Verificamos que el método privado funcionó
        historial = cuenta.obtener_historial()
        assert len(historial) == 2
        assert historial[0]["tipo"] == "DEPOSITO"
        assert historial[1]["tipo"] == "RETIRO"


class TestCoverageAvanzado:
    """Tests para demostrar conceptos avanzados de cobertura"""
    
    def test_statement_coverage_completo(self):
        """
        Intenta cubrir todas las líneas de código en el método transferir
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta1 = banco.crear_cuenta("111111", "Juan Pérez", 1000.0)
        cuenta2 = banco.crear_cuenta("222222", "Ana López", 500.0)
        
        # When - Transferencia exitosa (cubre path principal)
        resultado = banco.transferir("111111", "222222", 300.0)
        
        # Then
        assert resultado is True
        assert cuenta1.obtener_saldo() == 700.0
        assert cuenta2.obtener_saldo() == 800.0
        
        # Test para cubrir validación de cantidad negativa
        with pytest.raises(ValueError):
            banco.transferir("111111", "222222", -100.0)
        
        # Test para cubrir cuenta origen no encontrada
        with pytest.raises(CuentaNoEncontradaError):
            banco.transferir("999999", "222222", 100.0)
        
        # Test para cubrir cuenta destino no encontrada
        with pytest.raises(CuentaNoEncontradaError):
            banco.transferir("111111", "999999", 100.0)
        
        # Test para cubrir saldo insuficiente
        with pytest.raises(SaldoInsuficienteError):
            banco.transferir("111111", "222222", 1000.0)  # Solo tiene 700.0
    
    def test_edge_cases_coverage(self):
        """
        Cubre casos límite que podrían no estar cubiertos
        """
        # Given
        banco = Banco("Banco Nacional")
        
        # Edge case: Crear cuenta con saldo exactamente 0
        cuenta_cero = banco.crear_cuenta("000000", "Usuario Cero", 0.0)
        assert cuenta_cero.obtener_saldo() == 0.0
        
        # Edge case: Retirar exactamente todo el saldo
        cuenta_exacta = banco.crear_cuenta("111111", "Usuario Exacto", 100.0)
        resultado = cuenta_exacta.retirar(100.0)
        assert resultado is True
        assert cuenta_exacta.obtener_saldo() == 0.0
        
        # Edge case: Transferencia de cantidad muy pequeña
        cuenta_pequena1 = banco.crear_cuenta("222222", "Usuario A", 0.01)
        cuenta_pequena2 = banco.crear_cuenta("333333", "Usuario B", 0.0)
        resultado = banco.transferir("222222", "333333", 0.01)
        assert resultado is True
        assert cuenta_pequena1.obtener_saldo() == 0.0
        assert cuenta_pequena2.obtener_saldo() == 0.01
    
    def test_coverage_de_excepciones_personalizadas(self):
        """
        Asegura que todas las excepciones personalizadas sean cubiertas
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta = banco.crear_cuenta("123456", "Juan Pérez", 100.0)
        
        # Cubrir SaldoInsuficienteError en cuenta individual
        with pytest.raises(SaldoInsuficienteError):
            cuenta.retirar(200.0)
        
        # Cubrir SaldoInsuficienteError en transferencia
        cuenta2 = banco.crear_cuenta("654321", "Ana López", 50.0)
        with pytest.raises(SaldoInsuficienteError):
            banco.transferir("123456", "654321", 200.0)
        
        # Cubrir CuentaNoEncontradaError
        with pytest.raises(CuentaNoEncontradaError):
            banco.obtener_cuenta("999999")
        
        # Cubrir ValueError en creación de cuenta duplicada
        with pytest.raises(ValueError):
            banco.crear_cuenta("123456", "Otro Usuario", 100.0)


class TestCoverageAnalysis:
    """Tests para analizar y mejorar la cobertura"""
    
    def test_cobertura_metodos_getter(self):
        """
        Cubre todos los métodos getter que podrían ser olvidados
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta1 = banco.crear_cuenta("111111", "Juan Pérez", 1000.0)
        cuenta2 = banco.crear_cuenta("222222", "Ana López", 500.0)
        
        # When/Then - Cubrir todos los getters
        assert cuenta1.obtener_saldo() == 1000.0
        assert cuenta1.obtener_historial() == []
        assert banco.obtener_numero_cuentas() == 2
        assert banco.obtener_total_depositado() == 1500.0
        assert banco.obtener_cuenta("111111") == cuenta1
        
        # Después de algunas transacciones
        cuenta1.depositar(100.0)
        cuenta2.retirar(50.0)
        banco.transferir("111111", "222222", 200.0)
        
        assert len(cuenta1.obtener_historial()) == 2  # Depósito + retiro (transferencia)
        assert len(cuenta2.obtener_historial()) == 2  # Retiro + depósito (transferencia)
        assert banco.contador_transacciones == 1
    
    def test_cobertura_inicializacion_completa(self):
        """
        Cubre todos los paths de inicialización
        """
        # Inicialización con todos los parámetros
        cuenta1 = Cuenta("123456", "Juan Pérez", 1000.0)
        assert cuenta1.numero_cuenta == "123456"
        assert cuenta1.titular == "Juan Pérez"
        assert cuenta1.saldo == 1000.0
        assert cuenta1.historial_transacciones == []
        assert cuenta1.fecha_creacion is not None
        
        # Inicialización con saldo por defecto
        cuenta2 = Cuenta("654321", "Ana López")
        assert cuenta2.saldo == 0.0
        
        # Inicialización de banco
        banco = Banco("Banco Nacional")
        assert banco.nombre == "Banco Nacional"
        assert banco.cuentas == {}
        assert banco.contador_transacciones == 0


class TestCoverageEjercicioPractico:
    """Ejercicio práctico para los estudiantes"""
    
    def test_encontrar_codigo_no_cubierto(self):
        """
        TODO: Los estudiantes deben ejecutar este test con coverage
        y encontrar qué líneas NO están cubiertas
        
        Ejecutar: pytest --cov=src tests/test_ejercicio4_coverage.py::TestCoverageEjercicioPractico::test_encontrar_codigo_no_cubierto --cov-report=html
        """
        # Given
        banco = Banco("Banco Nacional")
        cuenta = banco.crear_cuenta("123456", "Juan Pérez", 100.0)
        
        # When - Operaciones básicas
        cuenta.depositar(50.0)
        
        # Then
        assert cuenta.obtener_saldo() == 150.0
        
        # PREGUNTA: ¿Qué líneas de código NO están siendo cubiertas?
        # TAREA: Agregar tests para cubrir esas líneas
    
    def test_mejorar_cobertura_metodo_privado(self):
        """
        TODO: Completar este test para mejorar la cobertura
        """
        # Los estudiantes deben:
        # 1. Ejecutar coverage y ver qué líneas del método _registrar_transaccion no están cubiertas
        # 2. Crear tests específicos para cubrir esas líneas
        # 3. Verificar que la cobertura mejora
        pass
    
    def test_cobertura_servicio_externo(self):
        """
        TODO: Completar este test para cubrir el servicio externo
        """
        # Los estudiantes deben:
        # 1. Crear tests que cubran tanto el caso exitoso como el de error
        # 2. Usar mocks para hacer el test determinístico
        # 3. Verificar que ambos paths están cubiertos
        pass 
