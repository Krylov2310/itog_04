from typing import List, Dict, Any, Tuple, Optional


class DeliveryPoint:
    def __init__(self, name: str, x: float, y: float, weight: float = 0.0, notes: str = ''):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight
        self.notes = notes

    def __repr__(self) -> str:
        return (f'Пункт выдачи: "{self.name}", (Координаты "X" = {self.x}, "Y" = {self.y}), '
                f'Загрузка: {self.weight} кг, Примечание: {self.notes}')

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "weight": self.weight,
            "notes": self.notes
        }
