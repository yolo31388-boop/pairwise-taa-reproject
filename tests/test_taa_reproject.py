import pytest
from render import taa_reproject as mod

CASES = [
    ("jitter", 'm.jitter_sequence(5, 8) == 5'),
    ("velocity", 'm.velocity_present(True, False) is True'),
    ("clip", 'm.neighborhood_clip(10, 0, 5) == 5'),
    ("disocc", 'm.disocclusion(0.1, 0.05) is True'),
    ("alpha", 'm.alpha_test(0.6, 0.5) is True'),
    ("hdr", 'm.hdr_weight(10, 5) == approx(0.1)'),
    ("resize", 'm.reset_on_resize(1920, 1920) is False'),
    ("motion", 'm.motion_class(True, True) == "mixed"'),
    ("overspeed", 'm.overspeed(3, 2) is True'),
    ("cut", 'm.cut_reset(True, "h") is None'),
    ("ui", 'm.ui_mask(True, 1) == 0'),
    ("camera", 'm.camera_history(1, "h") == "1:h"'),
    ("sharpen", 'm.sharpen_order(1, 2) is True'),
    ("blend", 'm.blend_weight(0.8, 0.5) == approx(0.4)'),
    ("clamp", 'm.clamp_axis(12, 0, 5) == 5')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
