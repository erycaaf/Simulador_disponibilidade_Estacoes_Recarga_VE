from datetime import datetime
from typing import Optional
import random


class SimulatedStation:
    def __init__(
            self,
            id: int,
            potencia: float,
            status: str,
            city: str = "",
            battery_percent: float = 20.0,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None):
        self.id = id
        self.potencia = potencia
        self.status = status
        self.city = city
        self.battery_percent = battery_percent
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_status(self, new_status: str):
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "ID": self.id,
            "Potencia": self.potencia,
            "Status": self.status,
            "City": self.city,
            "BatteryPercent": self.battery_percent,
            "CreatedAt": self.created_at.isoformat(),
            "UpdatedAt": self.updated_at.isoformat()
        }

    def copy(self):
        return SimulatedStation(
            id=self.id,
            potencia=self.potencia,
            status=self.status,
            city=self.city,
            battery_percent=self.battery_percent,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_dict(data: dict):
        # Extrai cidade do campo AddressInfo['Town'] se existir
        city = ""
        address_info = data.get("AddressInfo", {})
        if "Town" in address_info:
            city = address_info["Town"]
        if "Potencia" in data:
            potencia = data["Potencia"]
        else:
            ev_power_values_w = [
                7200, 7400, 9600, 11000, 19200, 22000,
                24000, 25000, 30000, 50000, 75000, 90000,
                100000, 120000, 150000, 175000, 200000,
                250000, 270000, 300000, 320000, 350000]
            potencia = random.choice(ev_power_values_w) / 1000.0  # kW

        # Status: se não definido, sorteia entre possíveis
        if "Status" in data:
            status = data["Status"]
        else:
            status_list = [
                "Available",
                "Operational",
                "Charging",
                "Out of Service"]
            status = random.choice(status_list)

        # Battery percent: default 20% if not present
        battery_percent = data.get("BatteryPercent", 20.0)

        return SimulatedStation(
            id=data.get("ID"),
            potencia=potencia,
            status=status,
            city=city,
            battery_percent=battery_percent,
            created_at=datetime.fromisoformat(
                data["CreatedAt"]) if "CreatedAt" in data else None,
            updated_at=datetime.fromisoformat(
                data["UpdatedAt"]) if "UpdatedAt" in data else None)
