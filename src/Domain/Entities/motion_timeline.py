from dataclasses import dataclass, field
from typing import Any
from src.Domain.Entities.media_layer import MediaLayer


@dataclass(frozen=True)
class Keyframe:
    time_ms: int
    properties: dict[str, Any]
    easing: str = "cubic-bezier(0.25, 0.1, 0.25, 1.0)"

    def __post_init__(self) -> None:
        if self.time_ms < 0:
            raise ValueError("Keyframe time_ms must be non-negative.")


@dataclass
class MotionTimeline:
    timeline_id: str
    name: str
    duration_ms: int
    delay_ms: int = 0
    keyframes: list[Keyframe] = field(default_factory=list)
    layers: list[MediaLayer] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.duration_ms <= 0:
            raise ValueError("Duration must be greater than 0 ms.")
        if self.delay_ms < 0:
            raise ValueError("Delay must be non-negative.")

    def add_keyframe(self, keyframe: Keyframe) -> None:
        if keyframe.time_ms > self.duration_ms:
            raise ValueError(
                f"Keyframe time_ms ({keyframe.time_ms}ms) exceeds timeline duration ({self.duration_ms}ms)."
            )
        self.keyframes.append(keyframe)

    def add_layer(self, layer: MediaLayer) -> None:
        if any(existing.layer_id == layer.layer_id for existing in self.layers):
            raise ValueError(f"Layer with id '{layer.layer_id}' already exists in timeline.")
        self.layers.append(layer)

    def get_keyframes_sorted(self) -> list[Keyframe]:
        return sorted(self.keyframes, key=lambda k: k.time_ms)

    @property
    def total_duration_ms(self) -> int:
        return self.duration_ms + self.delay_ms
