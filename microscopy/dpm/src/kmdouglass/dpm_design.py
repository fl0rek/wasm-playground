from enum import Enum
from typing import Any


class Units(Enum):
    mm = 1e-3
    um = 1e-6
    nm = 1e-9


data = {
    "objective.magnification": 20,
    "objective.numerical_aperture": 0.4,
    "camera.pixel_size": 5,
    "camera.pixel_size.units": Units.um,
    "light_source.wavelength": 0.64,
    "light_source.wavelength.units": Units.um,
    "grating.period": 1000/300,
    "grating.period.units": Units.um,
}


def resolution(data: dict[str, Any]) -> tuple[float, Units]:
    """Computes the radius of the Airy disk in the object space."""

    return (
        1.22 * data["light_source.wavelength"] / data["objective.numerical_aperture"],
        data["light_source.wavelength.units"],
    )


def maximum_grating_period(data: dict[str, Any]) -> tuple[float, Units]:
    """Computes the maximum period of the grating to ensure correct PSF sampling."""

    period = data["light_source.wavelength"] * data["objective.magnification"] / 3 / data["objective.numerical_aperture"]

    return period, data["light_source.wavelength.units"]


def minimum_4f_magnification(data: dict[str, Any]) -> tuple[float, Units]:
    px_size = data["camera.pixel_size"] * data["camera.pixel_size.units"].value
    gr_period = data["grating.period"] * data["grating.period.units"].value
    wav = data["light_source.wavelength"] * data["light_source.wavelength.units"].value

    mag = 2 * px_size* (1 / gr_period + data["objective.numerical_aperture"] / wav / data["objective.magnification"])

    return mag, None


if __name__ == "__main__":
    print(resolution(data))
    print(maximum_grating_period(data))
    print(minimum_4f_magnification(data))
