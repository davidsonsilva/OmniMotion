from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensions:
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("Width must be greater than 0.")
        if self.height <= 0:
            raise ValueError("Height must be greater than 0.")

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def scale(self, factor: float) -> "Dimensions":
        if factor <= 0:
            raise ValueError("Scale factor must be greater than 0.")
        return Dimensions(width=self.width * factor, height=self.height * factor)
