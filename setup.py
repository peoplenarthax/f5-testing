#!/usr/bin/env python3
"""
Script de configuración para el Taller de Testing
"""

import subprocess
import sys
import os

def run_command(command):
    """Ejecuta un comando y muestra el resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {command}")
            return True
        else:
            print(f"✗ Error ejecutando: {command}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error ejecutando: {command}")
        print(f"  Excepción: {e}")
        return False

def main():
    print("🐍 Configurando el Taller de Testing en Python...")
    print("="*50)
    
    # Verificar versión de Python
    print(f"Python versión: {sys.version}")
    
    if sys.version_info < (3, 8):
        print("⚠️  Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    dependencies = [
        "pytest>=8.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "requests>=2.31.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}"):
            print(f"❌ Error instalando {dep}")
            sys.exit(1)
    
    # Verificar instalación
    print("\n🧪 Verificando instalación...")
    
    if not run_command("python -c \"import pytest; print('pytest:', pytest.__version__)\""):
        print("❌ Error: pytest no está instalado correctamente")
        sys.exit(1)
    
    if not run_command("python -c \"from src.cuenta import Cuenta; print('Módulos del proyecto funcionando')\""):
        print("❌ Error: Los módulos del proyecto no funcionan correctamente")
        sys.exit(1)
    
    # Ejecutar una prueba simple
    print("\n🔍 Ejecutando prueba simple...")
    if not run_command("python -m pytest tests/test_ejercicio1_unit_testing.py::TestCuentaBasico::test_crear_cuenta_con_saldo_inicial -v"):
        print("❌ Error: Los tests no funcionan correctamente")
        sys.exit(1)
    
    print("\n🎉 ¡Instalación completada exitosamente!")
    print("\nPara comenzar el taller, ejecuta:")
    print("  python -m pytest tests/test_ejercicio1_unit_testing.py -v")
    print("\nPara ver todos los comandos disponibles, consulta el README.md")

if __name__ == "__main__":
    main() 
