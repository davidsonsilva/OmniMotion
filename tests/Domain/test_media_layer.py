import pytest
from src.Domain.Entities.media_layer import MediaLayer
from src.Domain.ValueObjects.dimensions import Dimensions


def test_media_layer_creation():
    dims = Dimensions(width=300.0, height=300.0)
    layer = MediaLayer(
        layer_id="webcam-1",
        name="Webcam Overlay",
        x=50.0,
        y=100.0,
        dimensions=dims,
        z_index=2,
        opacity=0.9,
        border_radius=16.0,
    )
    assert layer.layer_id == "webcam-1"
    assert layer.x == 50.0
    assert layer.y == 100.0
    assert layer.visible is True
    assert layer.opacity == 0.9
    assert layer.border_radius == 16.0


def test_media_layer_invalid_coordinates():
    dims = Dimensions(width=100.0, height=100.0)
    with pytest.raises(ValueError, match="X coordinate must be non-negative"):
        MediaLayer(
            layer_id="l1",
            name="Layer",
            x=-5.0,
            y=10.0,
            dimensions=dims,
        )

    with pytest.raises(ValueError, match="Y coordinate must be non-negative"):
        MediaLayer(
            layer_id="l1",
            name="Layer",
            x=10.0,
            y=-1.0,
            dimensions=dims,
        )


def test_media_layer_invalid_opacity():
    dims = Dimensions(width=100.0, height=100.0)
    with pytest.raises(ValueError, match="Opacity must be between 0.0 and 1.0"):
        MediaLayer(layer_id="l1", name="Layer", x=0, y=0, dimensions=dims, opacity=1.5)


def test_media_layer_invalid_border_radius():
    dims = Dimensions(width=100.0, height=100.0)
    with pytest.raises(ValueError, match="Border radius must be non-negative"):
        MediaLayer(layer_id="l1", name="Layer", x=0, y=0, dimensions=dims, border_radius=-4.0)


def test_media_layer_domain_methods():
    dims = Dimensions(width=100.0, height=100.0)
    layer = MediaLayer(layer_id="l1", name="Layer", x=10.0, y=10.0, dimensions=dims)

    layer.move_to(20.0, 30.0)
    assert layer.x == 20.0
    assert layer.y == 30.0

    new_dims = Dimensions(width=200.0, height=200.0)
    layer.resize(new_dims)
    assert layer.dimensions.width == 200.0

    layer.set_opacity(0.5)
    assert layer.opacity == 0.5

    layer.toggle_visibility()
    assert layer.visible is False
    layer.toggle_visibility()
    assert layer.visible is True
