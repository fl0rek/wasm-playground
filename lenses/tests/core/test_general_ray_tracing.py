from math import inf

import pytest

from ezray.core.general_ray_tracing import Conic, Image, Object, Toric


def test_conic_surface_negative_semi_diameter():
    with pytest.raises(ValueError):
        Conic(conic_constant=0, radius_of_curvature=100, semi_diameter=-1)


def test_toric_surface_negative_semi_diameter():
    with pytest.raises(ValueError):
        Toric(
            conic_constant=0,
            radius_of_curvature=100,
            semi_diameter=-1,
            radius_of_revolution=10,
        )


def test_toric_surface_negative_radius_of_revolution():
    with pytest.raises(ValueError):
        Toric(
            conic_constant=0,
            radius_of_curvature=100,
            semi_diameter=10,
            radius_of_revolution=-1,
        )


def test_object_surface_infinite_extent():
    surf = Object()
    assert surf.radius_of_curvature == inf
    assert surf.semi_diameter == inf


def test_image_surface_infinite_extent():
    surf = Image()
    assert surf.radius_of_curvature == inf
    assert surf.semi_diameter == inf
