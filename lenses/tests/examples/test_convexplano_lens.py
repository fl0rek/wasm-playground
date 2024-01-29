from ezray import trace
from ezray.examples.convexplano_lens import model, SPECS

import numpy as np


def test_trace_convexplano_lens():
    """Test the Convexplano lens."""
    rays = model.marginal_ray[0]
    results = trace(rays, model)

    assert results.shape == (len(model.surfaces), len(rays), 2)


def test_aperture_stop():
    assert model.aperture_stop == SPECS["aperture_stop"]


def test_entrance_pupil():
    assert model.entrance_pupil == SPECS["entrance_pupil"]


def test_marginal_ray():
    assert np.allclose(model.marginal_ray, SPECS["marginal_ray"], atol=1e-3)
