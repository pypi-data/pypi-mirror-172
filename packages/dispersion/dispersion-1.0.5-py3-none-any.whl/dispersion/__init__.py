import numpy as np
import sys
import warnings
from dispersion.spectrum import Spectrum
from dispersion.spectral_data import *
from dispersion.io import Writer, Reader
from dispersion.material import Material
from dispersion.catalogue import Catalogue, rebuild_catalogue
from dispersion.config import get_config, default_config

__version__ = "1.0.5"
__all__ = ["Spectrum", "Material", "Catalogue", "get_config",
           "Constant", "Interpolation", "Extrapolation",
           "Sellmeier", "Sellmeier2", "Polynomial",
           "RefractiveIndexInfo", "Cauchy", "Gases",
           "Herzberger", "Retro", "Exotic", "Drude",
           "DrudeLorentz", "rebuild_catalogue", "Writer", "Reader"]

try:
    config = get_config()
except ValueError:
    config = default_config()

try:
    from ruamel.yaml import YAML
    from ruamel.yaml import scalarstring
    from ruamel.yaml.comments import CommentedMap
except ModuleNotFoundError as exc:
    if config['WarnMissingPackages']:
        warnings.warn("preferred yaml package ruamel.yaml not installed, " +
                      "falling back to PyYAML, writing yaml files may give " +
                      "inconsistent round trip results")
