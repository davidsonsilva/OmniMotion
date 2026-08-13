import pytest
from src.Domain.Entities.motion_timeline import Keyframe, MotionTimeline
from src.Domain.Entities.media_layer import MediaLayer
from src.Domain.ValueObjects.dimensions import Dimensions


def test_keyframe_validation():
    kf = Keyframe(time_ms=500, properties={"x": 100, "y": 200})
    assert kf.time_ms == 500
    assert kf.properties == {"x": 100, "y": 200}
    assert kf.easing == "cubic-bezier(0.25, 0.1, 0.25, 1.0)"

    with pytest.raises(ValueError, match="Keyframe time_ms must be non-negative"):
        Keyframe(time_ms=-10, properties={})


def test_motion_timeline_creation():
    timeline = MotionTimeline(
        timeline_id="tl-1",
        name="Main Scene Motion",
        duration_ms=5000,
        delay_ms=200,
    )
    assert timeline.timeline_id == "tl-1"
    assert timeline.duration_ms == 5000
    assert timeline.delay_ms == 200
    assert timeline.total_duration_ms == 5200


def test_motion_timeline_invalid_duration_or_delay():
    with pytest.raises(ValueError, match="Duration must be greater than 0 ms"):
        MotionTimeline(timeline_id="t", name="T", duration_ms=0)

    with pytest.raises(ValueError, match="Delay must be non-negative"):
        MotionTimeline(timeline_id="t", name="T", duration_ms=1000, delay_ms=-50)


def test_motion_timeline_add_keyframe_and_sort():
    timeline = MotionTimeline(timeline_id="tl-1", name="Motion", duration_ms=3000)
    kf1 = Keyframe(time_ms=1500, properties={"opacity": 0.5})
    kf2 = Keyframe(time_ms=500, properties={"opacity": 0.0})
    kf3 = Keyframe(time_ms=2500, properties={"opacity": 1.0})

    timeline.add_keyframe(kf1)
    timeline.add_keyframe(kf2)
    timeline.add_keyframe(kf3)

    sorted_kfs = timeline.get_keyframes_sorted()
    assert [k.time_ms for k in sorted_kfs] == [500, 1500, 2500]


def test_motion_timeline_keyframe_exceeds_duration():
    timeline = MotionTimeline(timeline_id="tl-1", name="Motion", duration_ms=1000)
    invalid_kf = Keyframe(time_ms=1500, properties={})
    with pytest.raises(ValueError, match="exceeds timeline duration"):
        timeline.add_keyframe(invalid_kf)


def test_motion_timeline_add_layer():
    timeline = MotionTimeline(timeline_id="tl-1", name="Motion", duration_ms=1000)
    layer = MediaLayer(
        layer_id="webcam",
        name="Webcam",
        x=0,
        y=0,
        dimensions=Dimensions(100, 100),
    )
    timeline.add_layer(layer)
    assert len(timeline.layers) == 1

    with pytest.raises(ValueError, match="already exists in timeline"):
        timeline.add_layer(layer)
