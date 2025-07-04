# Taller de Testing en Python 🐍

## Sistema Bancario - Ejercicios de Testing

Este proyecto contiene un sistema bancario simple diseñado para aprender conceptos fundamentales de testing en Python. Está organizado en 4 ejercicios progresivos que cubren desde unit testing básico hasta conceptos avanzados como mocking y code coverage.

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Conceptos Clave](#conceptos-clave)
4. [Ejercicios](#ejercicios)
5. [Comandos Útiles](#comandos-útiles)
6. [Recursos Adicionales](#recursos-adicionales)

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-proyecto>
   cd f5-factoria-testing
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar la instalación**
   ```bash
   pytest --version
   ```

## 📁 Estructura del Proyecto

```
f5-factoria-testing/
├── src/
│   ├── __init__.py
│   ├── cuenta.py          # Clase Cuenta bancaria
│   └── banco.py           # Clase Banco que maneja múltiples cuentas
├── tests/
│   ├── __init__.py
│   ├── test_ejercicio1_unit_testing.py      # Unit Testing básico
│   ├── test_ejercicio2_integration_testing.py # Integration Testing
│   ├── test_ejercicio3_mocking_flaky.py     # Mocking y Flaky Tests
│   └── test_ejercicio4_coverage.py          # Code Coverage
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## 🎯 Conceptos Clave

### 1. **Given/When/Then** (Dado/Cuando/Entonces)
Patrón para estructurar tests de manera clara:
- **Given**: Configuración inicial (datos de entrada)
- **When**: Acción que se está probando
- **Then**: Verificación del resultado esperado

### 2. **Caja Negra (Black Box)**
Probar el comportamiento externo sin conocer la implementación interna.

### 3. **Software Under Test (SUT)**
El código o componente que estamos probando.

### 4. **Function vs Object Testing**
- **Function**: Probar funciones individuales
- **Object**: Probar el comportamiento de objetos completos

### 5. **Test Driven Development (TDD)**
Metodología donde se escriben los tests antes que el código.

## 📚 Ejercicios

### 🔹 Ejercicio 1: Unit Testing Básico

**Archivo**: `tests/test_ejercicio1_unit_testing.py`

**Conceptos cubiertos**:
- Patrón Given/When/Then
- Assertions básicas
- Testing de excepciones
- Diferencia entre función y objeto

**Ejemplos de tests**:
```python
def test_depositar_dinero_exitosamente(self):
    # Given
    cuenta = Cuenta("12345", "Juan Pérez", 100.0)
    cantidad_deposito = 50.0
    
    # When
    resultado = cuenta.depositar(cantidad_deposito)
    
    # Then
    assert resultado is True
    assert cuenta.obtener_saldo() == 150.0
```

**Ejecutar**:
```bash
pytest tests/test_ejercicio1_unit_testing.py -v
```

**Tareas para completar**:
1. `test_crear_cuenta_sin_saldo_inicial()`
2. `test_depositar_cero_debe_fallar()`

---

### 🔹 Ejercicio 2: Integration Testing

**Archivo**: `tests/test_ejercicio2_integration_testing.py`

**Conceptos cubiertos**:
- Integración entre múltiples componentes
- Testing de flujos completos
- Consistencia de estado entre objetos

**Ejemplos de tests**:
```python
def test_transferencia_entre_cuentas_exitosa(self):
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
```

**Ejecutar**:
```bash
pytest tests/test_ejercicio2_integration_testing.py -v
```

**Tareas para completar**:
1. `test_crear_banco_con_multiples_cuentas()`
2. `test_transferencia_circular_entre_tres_cuentas()`

---

### 🔹 Ejercicio 3: Mocking y Flaky Tests

**Archivo**: `tests/test_ejercicio3_mocking_flaky.py`

**Conceptos cubiertos**:
- Mocking de dependencias externas
- Stubbing de comportamientos
- Identificación y solución de flaky tests
- Manejo de comportamiento no determinístico

**Ejemplos de tests**:
```python
def test_mock_servicio_externo_exitoso(self):
    # Given
    banco = Banco("Banco Nacional")
    banco.crear_cuenta("123456", "Juan Pérez", 1000.0)
    
    # When - Mockeamos el servicio externo
    with patch.object(banco, 'validar_cuenta_con_servicio_externo', return_value=True):
        resultado = banco.validar_cuenta_con_servicio_externo("123456")
    
    # Then
    assert resultado is True
```

**Ejecutar**:
```bash
pytest tests/test_ejercicio3_mocking_flaky.py -v
```

**Tareas para completar**:
1. `test_mock_transferencia_con_validacion_externa()`
2. `test_solucionar_flaky_test_con_time_sleep()`

---

### 🔹 Ejercicio 4: Code Coverage

**Archivo**: `tests/test_ejercicio4_coverage.py`

**Conceptos cubiertos**:
- Cobertura de líneas (Line Coverage)
- Cobertura de ramas (Branch Coverage)
- Identificación de código no cubierto
- Análisis de cobertura

**Ejecutar con coverage**:
```bash
pytest tests/test_ejercicio4_coverage.py --cov=src --cov-report=html
```

**Tareas para completar**:
1. `test_mejorar_cobertura_metodo_privado()`
2. `test_cobertura_servicio_externo()`

## 🛠️ Comandos Útiles

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con información detallada
```bash
pytest -v
```

### Ejecutar un test específico
```bash
pytest tests/test_ejercicio1_unit_testing.py::TestCuentaBasico::test_depositar_dinero_exitosamente -v
```

### Ejecutar tests con coverage
```bash
pytest --cov=src
```

### Generar reporte de coverage en HTML
```bash
pytest --cov=src --cov-report=html
```

### Ejecutar tests y mostrar los más lentos
```bash
pytest --durations=10
```

### Ejecutar tests que fallan y parar en el primer fallo
```bash
pytest -x
```

### Ejecutar tests que contienen una palabra clave
```bash
pytest -k "depositar"
```

## 📝 Flujo de Trabajo del Taller

### Parte 1: Unit Testing (15 minutos)
1. Revisar el código de `src/cuenta.py`
2. Analizar los tests en `test_ejercicio1_unit_testing.py`
3. Completar los tests marcados con `TODO`
4. Ejecutar: `pytest tests/test_ejercicio1_unit_testing.py -v`

### Parte 2: Integration Testing (15 minutos)
1. Revisar el código de `src/banco.py`
2. Analizar los tests de integración
3. Completar los tests prácticos
4. Ejecutar: `pytest tests/test_ejercicio2_integration_testing.py -v`

### Parte 3: Mocking y Flaky Tests (15 minutos)
1. Entender el problema de los flaky tests
2. Aprender a usar mocks para dependencias externas
3. Completar los ejercicios prácticos
4. Ejecutar: `pytest tests/test_ejercicio3_mocking_flaky.py -v`

### Parte 4: Code Coverage (15 minutos)
1. Ejecutar tests con coverage
2. Analizar el reporte HTML
3. Identificar código no cubierto
4. Completar tests para mejorar cobertura

## 🎯 Objetivos de Aprendizaje

Al finalizar este taller, los participantes serán capaces de:

1. **Escribir unit tests** siguiendo el patrón Given/When/Then
2. **Crear integration tests** que verifiquen el funcionamiento conjunto de componentes
3. **Identificar y solucionar flaky tests** usando mocking y stubbing
4. **Analizar code coverage** e identificar código no cubierto por tests
5. **Aplicar principios de TDD** en el desarrollo de software

## 🔧 Troubleshooting

### Problemas Comunes

**Error: "ModuleNotFoundError: No module named 'src'"**
- Solución: Asegúrate de ejecutar pytest desde el directorio raíz del proyecto

**Error: "pytest: command not found"**
- Solución: Instala pytest con `pip install pytest`

**Tests fallan aleatoriamente**
- Causa: Probable flaky test
- Solución: Usar mocks para eliminar la aleatoriedad

### Verificar que todo funciona
```bash
# Ejecutar todos los tests
pytest

# Debería mostrar algo como:
# ===== X passed, Y skipped in Z.ZZs =====
```

## 📖 Recursos Adicionales

- [Documentación oficial de pytest](https://docs.pytest.org/)
- [Python Testing 101](https://realpython.com/python-testing/)
- [Mocking en Python](https://docs.python.org/3/library/unittest.mock.html)
- [Test-Driven Development](https://testdriven.io/test-driven-development/)

## 🤝 Contribuciones

Si encuentras algún error o tienes sugerencias para mejorar el taller, no dudes en abrir un issue o enviar un pull request.

---

**¡Feliz Testing! 🧪✨** 
