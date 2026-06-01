"""
Core Microgrid Components
Defines base classes for microgrid elements
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict
import numpy as np
from enum import Enum


class OperatingMode(Enum):
    """Operating modes of the microgrid"""
    GRID_CONNECTED = "grid_connected"
    ISLANDED = "islanded"
    TRANSITIONAL = "transitional"


@dataclass
class BusState:
    """State variables of a bus"""
    voltage_magnitude: float  # V
    voltage_angle: float     # radians
    frequency: float         # Hz
    power_injection: float   # W (active power)
    reactive_power: float    # VAR


@dataclass
class FaultData:
    """Fault information"""
    fault_location: int      # Bus ID
    fault_type: str         # "3P", "2P", "1P", "HIF"
    inception_time: float   # seconds
    fault_current: float    # A
    fault_impedance: float  # Ohms


class MicrogridBus:
    """Represents a bus in the microgrid"""
    
    def __init__(self, bus_id: int, nominal_voltage: float):
        self.bus_id = bus_id
        self.nominal_voltage = nominal_voltage
        self.state = BusState(
            voltage_magnitude=nominal_voltage,
            voltage_angle=0.0,
            frequency=60.0,
            power_injection=0.0,
            reactive_power=0.0
        )
        self.connected_devices = []
    
    def add_device(self, device):
        """Connect a device to this bus"""
        self.connected_devices.append(device)
    
    def update_state(self, voltage_mag, voltage_angle, frequency):
        """Update bus state"""
        self.state.voltage_magnitude = voltage_mag
        self.state.voltage_angle = voltage_angle
        self.state.frequency = frequency


class Microgrid:
    """Main microgrid class"""
    
    def __init__(self, name: str):
        self.name = name
        self.buses: Dict[int, MicrogridBus] = {}
        self.lines: List = []
        self.operating_mode = OperatingMode.GRID_CONNECTED
        self.frequency = 60.0
        self.timestamp = 0.0
    
    def add_bus(self, bus_id: int, nominal_voltage: float) -> MicrogridBus:
        """Add a bus to the microgrid"""
        bus = MicrogridBus(bus_id, nominal_voltage)
        self.buses[bus_id] = bus
        return bus
    
    def get_bus(self, bus_id: int) -> MicrogridBus:
        """Get a bus by ID"""
        return self.buses.get(bus_id)
    
    def set_operating_mode(self, mode: OperatingMode):
        """Change operating mode"""
        self.operating_mode = mode
    
    def get_bus_states(self) -> Dict[int, BusState]:
        """Get all bus states"""
        return {bus_id: bus.state for bus_id, bus in self.buses.items()}
