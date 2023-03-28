from enum import Enum
from typing import Any, Optional, TypedDict


class Units(Enum):
    mm = 1e-3
    um = 1e-6


class Result(TypedDict):
    value: float
    units: Optional[Units]
    name: str
    equation: str


inputs = {
    "objective.magnification": 20,
    "objective.numerical_aperture": 0.4,
    "camera.pixel_size": 5.2,
    "camera.pixel_size.units": Units.um,
    "camera.horizontal_number_of_pixels": 512,
    "camera.vertical_number_of_pixels": 512,
    "light_source.wavelength": 0.64,
    "light_source.wavelength.units": Units.um,
    "grating.period": 1000/300,
    "grating.period.units": Units.um,
    "lens_1.focal_length": 75,
    "lens_1.focal_length.units": Units.mm,
    "lens_1.clear_aperture": 45.72,
    "lens_1.clear_aperture.units": Units.mm,
    "lens_2.focal_length": 300,
    "lens_2.focal_length.units": Units.mm,
    "lens_2.clear_aperture": 45.72,
    "lens_2.clear_aperture.units": Units.mm,
    "pinhole.diameter": 30,
    "pinhole.diameter.units": Units.um,
    "misc.central_lobe_size_factor": 4,
}


def resolution(inputs: dict[str, Any]) -> Result:
    """Computes the radius of the Airy disk in the object space."""

    units = Units.um
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    value = 1.22 * wav / inputs["objective.numerical_aperture"] / units.value

    return {
        "value": value,
        "units": units,
        "name": "Resolution",
        "equation": r"\( \Delta \rho = \frac{ 1.22 \lambda }{ \text{NA}_{obj} }\)"
    }


def minimum_resolution(inputs: dict[str, Any]) -> Result:
    """Computes the minimum radius of the Airy disk in the object space for a given grating and objective magnification."""

    units = Units.um
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value
    value = gr_period / Units.um.value / 0.28 / inputs["objective.magnification"]

    return {
       "value": value,
       "units": units,
       "name": "Minimum resolution",
       "equation": r"\( \Delta \rho \ge \frac{\Lambda}{0.28 M_{obj}}  \)",
    }


def maximum_grating_period(inputs: dict[str, Any]) -> Result:
    """Computes the maximum period of the grating to ensure correct PSF sampling."""

    units = Units.um
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    value = wav * inputs["objective.magnification"] / 3 / inputs["objective.numerical_aperture"] / units.value

    return {
        "value": value,
        "units": units,
        "name": "Maximum grating period",
        "equation": r"\(\Lambda \le \frac{ \lambda M_{obj} }{3 \text{NA}_{obj}}\)"
    }


def maximum_pixel_size(inputs: dict[str, Any]) -> Result:
    """Computes the maximum pixel size that satisfies the sampling requirements given a grating period."""

    units = Units.um
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value
    mag_4f = actual_4f_magnification(inputs)["value"]
    value = gr_period * abs(mag_4f) / 2.67 / units.value

    return {
        "value": value,
        "units": units,
        "name": "Maximum pixel size",
        "equation": r"\( a \le \frac{ \Lambda |M_{4f}| }{ 2.67 }\)",
    }


def fourier_plane_spacing(inputs: dict[str, Any]) -> Result:
    """The position of the first diffraction order in the Fourier plane with respect to the optics axis.

    This assumes that the tangent of the diffracted angle is approximately equal to the angle itself.

    """

    units = Units.mm
    f1 = inputs["lens_1.focal_length"] * inputs["lens_1.focal_length.units"].value
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value
    value = f1 * wav / gr_period / units.value

    return {
        "value": value,
        "units": units,
        "name": "Fourier plane spacing",
        "equation": r"\( \Delta x = \frac{ f_1 \lambda }{ \Lambda } \)"
    }


def minimum_4f_magnification(inputs: dict[str, Any]) -> Result:
    """Computes the minimum magnification of the 4f system for sufficient PSF/fringe sampling."""

    units = None
    px_size = inputs["camera.pixel_size"] * inputs["camera.pixel_size.units"].value
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value

    value = 2 * px_size* (1 / gr_period + inputs["objective.numerical_aperture"] / wav / inputs["objective.magnification"])

    return {
        "value": value,
        "units": units,
        "name": "Minimum 4f magnification (abs. value)",
        "equation": r"\( |M_{4f}| \ge 2a \left( \frac{1}{\Lambda} + \frac{ \text{NA}_{obj} }{ \lambda M_{obj} } \right) \)"
    }


def actual_4f_magnification(inputs: dict[str, Any]) -> Result:
    """Computes the actual magnification of the 4f system."""

    units = None
    f1 = inputs["lens_1.focal_length"] * inputs["lens_1.focal_length.units"].value
    f2 = inputs["lens_2.focal_length"] * inputs["lens_2.focal_length.units"].value
    value = -f2 / f1

    return {
        "value": value,
        "units": units,
        "name": "Actual 4f magnification",
        "equation": r"\( -f_2 / f_1 \)",
    }


def system_magnification(inputs: dict[str, Any]) -> Result:
    """Computes the magnification of the entire system."""

    units = None
    mag_4f = actual_4f_magnification(inputs)["value"]
    value = -inputs["objective.magnification"] * mag_4f

    return {
        "value": value,
        "units": units,
        "name": "System magnification",
        "equation": r"\( M_{obj} M_{4f} \)",
    }


def field_of_view_horizontal(inputs: dict[str, Any]) -> Result:
    """Computes the horizontal field of view in the object space."""

    units = Units.um
    px_size = inputs["camera.pixel_size"] * inputs["camera.pixel_size.units"].value
    mag_4f = actual_4f_magnification(inputs)["value"]

    value = inputs["camera.horizontal_number_of_pixels"] * px_size / inputs["objective.magnification"] / abs(mag_4f) / units.value

    return {
        "value": value,
        "units": units,
        "name": "Field of view (horizontal)",
        "equation": r"\( \text{FOV}_h = m \frac{ a } { M_{obj} |M_{4f}| } \)",
    }


def field_of_view_vertical(inputs: dict[str, Any]) -> Result:
    """Computes the vertical field of view in the object space."""

    units = Units.um
    px_size = inputs["camera.pixel_size"] * inputs["camera.pixel_size.units"].value
    mag_4f = actual_4f_magnification(inputs)["value"]

    value = inputs["camera.vertical_number_of_pixels"] * px_size / inputs["objective.magnification"] / abs(mag_4f) / units.value

    return {
        "value": value,
        "units": units,
        "name": "Field of view (vertical)",
        "equation": r"\( \text{FOV}_v = n \frac{ a } { M_{obj} |M_{4f}| } \)",
    }


def camera_diagonal(inputs: dict[str, Any]) -> Result:
    """Computes the length of the diagonal across the camera."""

    units = Units.mm
    px_size = inputs["camera.pixel_size"] * inputs["camera.pixel_size.units"].value
    num_px_h = inputs["camera.horizontal_number_of_pixels"]
    num_px_v = inputs["camera.vertical_number_of_pixels"]

    value = px_size * (num_px_h**2 + num_px_v**2)**(0.5) / units.value

    return {
        "value": value,
        "units": units,
        "name": "Camera diagonal",
        "equation": r"\( D = a \sqrt{m^2 + n^2} \)",
    }


def minimum_lens_1_na(inputs: dict[str, Any]) -> Result:
    """Computes the minimum NA of the first Fourier lens to avoid clipping the +1 diffracted order."""

    units = None
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value

    value = wav / gr_period +  inputs["objective.numerical_aperture"] / inputs["objective.magnification"]

    return {
        "value": value,
        "units": units,
        "name": "Minimum NA of Fourier lens 1",
        "equation": r"\( \text{NA}_{L_1} \ge \frac{ \lambda }{ \Lambda } + \frac{\text{NA}_{obj}}{M_{obj}} \)",
    }


def minimum_lens_2_na(inputs: dict[str, Any]) -> Result:
    """Computes the minimum NA of the second Fourier lens to avoid clipping the +1 diffracted order."""

    units = None
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    gr_period = inputs["grating.period"] * inputs["grating.period.units"].value
    mag_4f = actual_4f_magnification(inputs)["value"]
    pinhole_diam = inputs["pinhole.diameter"] * inputs["pinhole.diameter.units"].value

    value =  wav / abs(mag_4f) / gr_period + 1.22 * wav / pinhole_diam

    return {
        "value": value,
        "units": units,
        "name": "Minimum NA of Fourier lens 2",
        "equation": r"\( \text{NA}_{L_2} \ge \frac{ \lambda }{ \Lambda |M_{4f}| } + 1.22 \frac{ \lambda} { d } \)",
    }


def lens_na(focal_length: float, clear_aperture: float) -> float:
    """Computes the NA of a lens assuming the Abbe sine condition is valid."""

    return clear_aperture / 2 / focal_length


def lens_1_na(inputs: dict[str, Any]) -> Result:
    """Computes the NA of the first Fourier lens."""

    units = None
    f1 = inputs["lens_1.focal_length"] * inputs["lens_1.focal_length.units"].value
    D = inputs["lens_1.clear_aperture"] * inputs["lens_1.clear_aperture.units"].value

    value = lens_na(f1, D)

    return {
        "value": value,
        "units": units,
        "name": "Actual NA of Fourier lens 1",
        "equation": r"\( \text{NA}_{L_1} = \frac{ D_1 }{ 2 f_1 } \)",
    }


def lens_2_na(inputs: dict[str, Any]) -> Result:
    """Computes the NA of the second Fourier lens."""

    units = None
    f2 = inputs["lens_2.focal_length"] * inputs["lens_2.focal_length.units"].value
    D = inputs["lens_2.clear_aperture"] * inputs["lens_2.clear_aperture.units"].value

    value = lens_na(f2, D)

    return {
        "value": value,
        "units": units,
        "name": "Actual NA of Fourier lens 2",
        "equation": r"\( \text{NA}_{L_2} = \frac{ D_2 }{ 2 f_2 } \)",
    }


def maximum_pinhole_diameter(inputs: dict[str, Any]) -> Result:
    """Compute the maximum pinhole diameter that ensures a uniform reference beam."""

    units = Units.um
    wav = inputs["light_source.wavelength"] * inputs["light_source.wavelength.units"].value
    f2 = inputs["lens_2.focal_length"] * inputs["lens_2.focal_length.units"].value
    cam_diag = camera_diagonal(inputs)
    cam_diag_norm = cam_diag["value"] * cam_diag["units"].value

    value = 2.44 * wav * f2 / cam_diag_norm / inputs["misc.central_lobe_size_factor"] / units.value

    return {
        "value": value,
        "units": units,
        "name": "Maximum pinhole diameter",
        "equation": r"\( d \le \frac{ 2.44 \lambda f_2 } { \gamma D} \)",
    }


def coupling_ratio(inputs: dict[str, Any]) -> Result:
    """Computes the ratio of the unscattered and scattered light beam radii in the Fourier plane.

    Notes
    -----

    > A ratio of 1 means that the diffraction spot is the same size as the FOV and only the DC
    > signal can be obtained. As the ratio approaches zero, more and more detail can be observed
    > within the image for a given FOV. [1]_

    .. [1] Bhaduri, et al., "Diffraction phase microscopy: principles and applications in materials
    and life sciences," Advances in Optics and Photonics 6, 57 (2014)

    """

    units = None

    res = resolution(inputs)
    fov_h = field_of_view_horizontal(inputs)
    fov_v = field_of_view_vertical(inputs)

    res_norm = res["value"] * res["units"].value
    fov_diag = ((fov_h["value"] * fov_h["units"].value)**2 + (fov_v["value"] * fov_v["units"].value)**2)**(0.5)

    value = res_norm / fov_diag

    return {
        "value": value,
        "units": units,
        "name": "Coupling ratio",
        "equation": r"\( \eta = \frac{ \Delta \rho }{ \text{FOV}_{\text{diagonal}}} \)",
    }


def compute_results(inputs: dict[str, Any]) -> dict[str, Any]:
    """Performs all design computations."""

    return {
        "resolution": resolution(inputs),
        "minimum_resolution": minimum_resolution(inputs),
        "camera_diagonal": camera_diagonal(inputs),
        "maximum_pixel_size": maximum_pixel_size(inputs),
        "field_of_view_horizontal": field_of_view_horizontal(inputs),
        "field_of_view_vertical": field_of_view_vertical(inputs),
        "maximum_grating_period": maximum_grating_period(inputs),
        "fourier_plane_spacing": fourier_plane_spacing(inputs),
        "minimum_lens_1_na": minimum_lens_1_na(inputs),
        "minimum_lens_2_na": minimum_lens_2_na(inputs),
        "lens_1_na": lens_1_na(inputs),
        "lens_2_na": lens_2_na(inputs),
        "minimum_4f_magnification": minimum_4f_magnification(inputs),
        "4f_magnification": actual_4f_magnification(inputs),
        "system_magnification": system_magnification(inputs),
        "maximum_pinhole_diameter": maximum_pinhole_diameter(inputs),
        "coupling_ratio": coupling_ratio(inputs),
    }


def validate_lens_2_na(_, results: dict[str, Any]) -> str:
    """Validates that the NA of lens 2 exceeds the minimum requirement."""
    
    lens_2_na = results["lens_2_na"]["value"]
    min_lens_2_na = results["minimum_lens_2_na"]["value"]

    if lens_2_na < min_lens_2_na:
        return f"NA of lens 2 is less than the minimum requirement: Minimum: {min_lens_2_na}, Actual: {lens_2_na}"
    
    return ""


def validate_results(inputs: dict[str, Any], results: dict[str, Any]) -> list[str]:
    """Validates whether the design criteria are satisfied."""

    violations = []
    violations.append(validate_lens_2_na(inputs, results))

    return violations


if __name__ == "__main__":
    from jinja2 import Environment, FileSystemLoader

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("design.html")

    results = compute_results(inputs)
    violations = validate_results(inputs, results)

    content = template.render(inputs=inputs, results=results, violations=violations)

    with open("output.html", mode="w", encoding="utf-8") as file:
        file.write(content)
