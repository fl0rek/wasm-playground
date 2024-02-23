from ezray.examples.convexplano_lens import paraxial_model, SPECS

import numpy as np


ATOL = 1e-3


def test_aperture_stop():
    assert paraxial_model.aperture_stop == SPECS["aperture_stop"]


def test_back_focal_length():
    assert np.allclose(
        paraxial_model.back_focal_length, SPECS["back_focal_length"], atol=ATOL
    )


def test_back_principal_plane():
    assert np.allclose(
        paraxial_model.back_principal_plane, SPECS["back_principal_plane"], atol=ATOL
    )


def test_effective_focal_length():
    assert np.allclose(
        paraxial_model.effective_focal_length,
        SPECS["effective_focal_length"],
        atol=ATOL,
    )


def test_entrance_pupil():
    assert np.allclose(
        paraxial_model.entrance_pupil.location,
        SPECS["entrance_pupil"].location,
        atol=ATOL,
    )
    assert np.allclose(
        paraxial_model.entrance_pupil.semi_diameter,
        SPECS["entrance_pupil"].semi_diameter,
        atol=ATOL,
    )


def test_exit_pupil():
    assert np.allclose(
        paraxial_model.exit_pupil.location, SPECS["exit_pupil"].location, atol=ATOL
    )
    assert np.allclose(
        paraxial_model.exit_pupil.semi_diameter,
        SPECS["exit_pupil"].semi_diameter,
        atol=ATOL,
    )


def test_front_focal_length():
    assert np.allclose(
        paraxial_model.front_focal_length, SPECS["front_focal_length"], atol=ATOL
    )


def test_front_principal_plane():
    assert np.allclose(
        paraxial_model.front_principal_plane, SPECS["front_principal_plane"], atol=ATOL
    )


def test_marginal_ray():
    assert np.allclose(paraxial_model.marginal_ray, SPECS["marginal_ray"], atol=ATOL)
