from dataclasses import dataclass
from src.Domain.ValueObjects.dimensions import Dimensions


@dataclass
class MediaLayer:
    layer_id: str
    name: str
    x: float
    y: float
    dimensions: Dimensions
    z_index: int = 0
    visible: bool = True
    opacity: float = 1.0
    border_radius: float = 0.0

    def __post_init__(self) -> None:
        if self.x < 0:
            raise ValueError("X coordinate must be non-negative (x >= 0).")
        if self.y < 0:
            raise ValueError("Y coordinate must be non-negative (y >= 0).")
        if not (0.0 <= self.opacity <= 1.0):
            raise ValueError("Opacity must be between 0.0 and 1.0.")
        if self.border_radius < 0:
            raise ValueError("Border radius must be non-negative.")

    def move_to(self, new_x: float, new_y: float) -> None:
        if new_x < 0 or new_y < 0:
            raise ValueError("New coordinates must be non-negative (x >= 0, y >= 0).")
        self.x = new_x
        self.y = new_y

    def resize(self, new_dimensions: Dimensions) -> None:
        if not isinstance(new_dimensions, Dimensions):
            raise TypeError("Dimensions must be an instance of Dimensions Value Object.")
        self.dimensions = new_dimensions

    def set_opacity(self, new_opacity: float) -> None:
        if not (0.0 <= new_opacity <= 1.0):
            raise ValueError("Opacity must be between 0.0 and 1.0.")
        self.opacity = new_opacity

    def toggle_visibility(self) -> None:
        self.visible = not self.visible
