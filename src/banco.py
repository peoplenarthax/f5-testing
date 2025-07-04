"""
Módulo de Banco
Sistema para manejar múltiples cuentas y transferencias
"""

import random
import time
from typing import Dict, Optional
from .cuenta import Cuenta, SaldoInsuficienteError


class CuentaNoEncontradaError(Exception):
    """Error cuando no se encuentra una cuenta"""
    pass


class ServicioExternoError(Exception):
    """Error cuando el servicio externo no está disponible"""
    pass


class Banco:
    """Clase que representa un banco con múltiples cuentas"""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuentas: Dict[str, Cuenta] = {}
        self.contador_transacciones = 0
    
    def crear_cuenta(self, numero_cuenta: str, titular: str, saldo_inicial: float = 0.0) -> Cuenta:
        """Crea una nueva cuenta bancaria"""
        if numero_cuenta in self.cuentas:
            raise ValueError(f"La cuenta {numero_cuenta} ya existe")
        
        cuenta = Cuenta(numero_cuenta, titular, saldo_inicial)
        self.cuentas[numero_cuenta] = cuenta
        return cuenta
    
    def obtener_cuenta(self, numero_cuenta: str) -> Cuenta:
        """Obtiene una cuenta por su número"""
        if numero_cuenta not in self.cuentas:
            raise CuentaNoEncontradaError(f"Cuenta {numero_cuenta} no encontrada")
        return self.cuentas[numero_cuenta]
    
    def transferir(self, numero_cuenta_origen: str, numero_cuenta_destino: str, cantidad: float) -> bool:
        """Transfiere dinero entre dos cuentas"""
        if cantidad <= 0:
            raise ValueError("La cantidad a transferir debe ser positiva")
        
        cuenta_origen = self.obtener_cuenta(numero_cuenta_origen)
        cuenta_destino = self.obtener_cuenta(numero_cuenta_destino)
        
        # Verificar saldo suficiente
        if cuenta_origen.obtener_saldo() < cantidad:
            raise SaldoInsuficienteError("Saldo insuficiente para la transferencia")
        
        # Realizar transferencia
        cuenta_origen.retirar(cantidad)
        cuenta_destino.depositar(cantidad)
        
        self.contador_transacciones += 1
        return True
    
    def obtener_total_depositado(self) -> float:
        """Obtiene el total de dinero depositado en todas las cuentas"""
        return sum(cuenta.obtener_saldo() for cuenta in self.cuentas.values())
    
    def validar_cuenta_con_servicio_externo(self, numero_cuenta: str) -> bool:
        """Simula la validación de una cuenta con un servicio externo"""
        # Simulamos latencia de red
        time.sleep(0.1)
        
        # Simulamos respuesta no determinística (flaky test)
        if random.random() < 0.1:  # 10% de probabilidad de fallo
            raise ServicioExternoError("Servicio de validación no disponible")
        
        # Simulamos validación exitosa
        return numero_cuenta in self.cuentas
    
    def obtener_numero_cuentas(self) -> int:
        """Obtiene el número total de cuentas"""
        return len(self.cuentas) 
