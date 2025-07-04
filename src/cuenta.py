"""
Módulo de Cuenta Bancaria
Sistema simple para el taller de testing
"""

from datetime import datetime
from typing import List


class SaldoInsuficienteError(Exception):
    """Error cuando se intenta retirar más dinero del disponible"""
    pass


class Cuenta:
    """Clase que representa una cuenta bancaria básica"""
    
    def __init__(self, numero_cuenta: str, titular: str, saldo_inicial: float = 0.0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo_inicial
        self.historial_transacciones = []
        self.fecha_creacion = datetime.now()
    
    def depositar(self, cantidad: float) -> bool:
        """Deposita dinero en la cuenta"""
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva")
        
        self.saldo += cantidad
        self._registrar_transaccion("DEPOSITO", cantidad)
        return True
    
    def retirar(self, cantidad: float) -> bool:
        """Retira dinero de la cuenta"""
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva")
        
        if cantidad > self.saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar la operación")
        
        self.saldo -= cantidad
        self._registrar_transaccion("RETIRO", cantidad)
        return True
    
    def obtener_saldo(self) -> float:
        """Obtiene el saldo actual de la cuenta"""
        return self.saldo
    
    def obtener_historial(self) -> List[dict]:
        """Obtiene el historial de transacciones"""
        return self.historial_transacciones.copy()
    
    def _registrar_transaccion(self, tipo: str, cantidad: float):
        """Registra una transacción en el historial"""
        transaccion = {
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": datetime.now(),
            "saldo_anterior": self.saldo - cantidad if tipo == "DEPOSITO" else self.saldo + cantidad,
            "saldo_nuevo": self.saldo
        }
        self.historial_transacciones.append(transaccion) 
