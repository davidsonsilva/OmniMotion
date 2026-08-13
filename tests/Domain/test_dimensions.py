import pytest
from src.Domain.ValueObjects.dimensions import Dimensions


def test_dimensions_valid_creation():
    dims = Dimensions(width=1920.0, height=1080.0)
    assert dims.width == 1920.0
    assert dims.height == 1080.0
    assert pytest.approx(dims.aspect_ratio, 0.01) == 1.777


def test_dimensions_invalid_width():
    with pytest.raises(ValueError, match="Width must be greater than 0"):
        Dimensions(width=0, height=1080.0)

    with pytest.raises(ValueError, match="Width must be greater than 0"):
        Dimensions(width=-100, height=1080.0)


def test_dimensions_invalid_height():
    with pytest.raises(ValueError, match="Height must be greater than 0"):
        Dimensions(width=1920.0, height=0)

    with pytest.raises(ValueError, match="Height must be greater than 0"):
        Dimensions(width=1920.0, height=-10)


def test_dimensions_immutability():
    dims = Dimensions(width=100.0, height=200.0)
    with pytest.raises(AttributeError):
        dims.width = 300.0  # Frozen dataclass


def test_dimensions_scale():
    dims = Dimensions(width=100.0, height=200.0)
    scaled = dims.scale(2.5)
    assert scaled.width == 250.0
    assert scaled.height == 500.0

    with pytest.raises(ValueError, match="Scale factor must be greater than 0"):
        dims.scale(0)
