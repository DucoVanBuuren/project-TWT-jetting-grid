#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""config_proto_opensimplex.py

User-configurable parameters for the generation of a jetting protocol using
OpenSimplex noise.

Two different sets of OpenSimplex noise can be mixed together: set A and set B.
You could specify a larger typical length scale for set B than for set A,
as specified by `FEATURE_SIZE`. Likewise the same for the typical time scale as
specified by `T_STEP`.

If `FEATURE_SIZE_B` is set to 0, set B will be completely ignored and no mixing
will take place.

Below settings will get stored inside the header section of the generated
protocol textfile.
"""
# ------------------------------------------------------------------------------
#  Start of user-configurable parameters
# ------------------------------------------------------------------------------

# Filename without extension for exporting the generated protocol files to disk
EXPORT_SUBFOLDER = "protocols"
EXPORT_FILENAME = "simplex_004"

# Number of frames (i.e. protocol lines) to generate.
# Do need exceed 5000 as this hits the memory limit of the microcontroller.
N_FRAMES = 5000  # Leave it at 5000

# Time interval between each frame [s].
DT_FRAME = 0.05  # Leave it at 0.05

# OpenSimplex noise coherent feature size [arb. unit, try ~ 50]
FEATURE_SIZE_A = 50
FEATURE_SIZE_B = 100

# OpenSimplex noise time step size [arb. unit, try ~ 0.1]
T_STEP_A = 0.1
T_STEP_B = 0.1

# OpenSimplex noise seeds
SEED_A = 1
SEED_B = 13

# To determine which valves should be opened and which ones should be closed, we
# apply a threshold function on each generated OpenSimplex noise [0-1]-grayscale
# image frame. In essence, we binarize each noise frame into a boolean black and
# white (BW) map. If a valve lies inside the `True` region it will get opened,
# otherwise it will get closed.
#
# Two different thresholding schemes exist.
# --> YOU MUST SPECIFY A VALUE FOR ONE SCHEME ONLY AND SET THE OTHER TO `None`.
#
# 1) Constant threshold
# ---------------------
# The applied threshold is constant for all image frames. Grayscale values above
# `1 - BW_threshold` will be set `True`. [grayscale value, 0-1].
BW_THRESHOLD = None  # Leave it at None. Use `TARGET_TRANSPARENCY` instead.

# 2) Newton solver
# ----------------
# A Newton solver is employed per image frame to try solve for the grayscale
# threshold that would result in the given target transparency. Transparency is
# defined as the number of `True / 1 / valve on` elements over the total number
# of elements. This method tends to minimize the fluctuation of the resulting
# valve transparency over each frame. [ratio, 0-1].
TARGET_TRANSPARENCY = 0.4

# Minimum valve on/off duration [number of frames].
# The originally generated valve durations can be automatically post-processed
# to ensure a minimum time duration between opening and closing each valve. When
# set to 0 or 1, no adjustment to the valve durations will be made.
# Tests show that the minimum valve duration is best kept at >= 0.25 seconds.
MIN_VALVE_DURATION = 5

# ------------------------------------------------------------------------------
#  End of user-configurable parameters
#  DO NOT ADJUST THE CODE FOLLOWING BELOW
# ------------------------------------------------------------------------------
# pylint: disable=wrong-import-position, invalid-name, missing-function-docstring

__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/project-TWT-jetting-grid"
__date__ = "18-04-2023"
__version__ = "1.0"  # Export file header info. Bump when major changes occur

import os as _os
from datetime import datetime

import numpy as _np

import constants as C

# Pixel distance between the integer PCS coordinates.
# Too large -> memory intense. Too small -> poor quality.
# 32 is a good value. Leave it.
PCS_PIXEL_DIST = 32
N_PIXELS = PCS_PIXEL_DIST * (C.NUMEL_PCS_AXIS + 1)

# Derived
X_STEP_A = _np.divide(1, FEATURE_SIZE_A * PCS_PIXEL_DIST / 32)
if FEATURE_SIZE_B != 0:
    X_STEP_B = _np.divide(1, FEATURE_SIZE_B * PCS_PIXEL_DIST / 32)
else:
    X_STEP_B = 0

if EXPORT_SUBFOLDER.strip() == "":
    EXPORT_PATH_NO_EXT = EXPORT_FILENAME
else:
    EXPORT_PATH_NO_EXT = _os.path.join(EXPORT_SUBFOLDER, EXPORT_FILENAME)

# ------------------------------------------------------------------------------
#  Valve transformations
# ------------------------------------------------------------------------------
# NOTE: The valve index of below arrays does /not/ indicate the valve number as
# laid out in the lab, but instead is simply linearly increasing.

# Create a map holding the pixel locations inside the noise image corresponding
# to each valve location
_pxs = _np.arange(
    PCS_PIXEL_DIST - 1, N_PIXELS - (PCS_PIXEL_DIST - 1), PCS_PIXEL_DIST
)
_grid_x, _grid_y = _np.meshgrid(_pxs, _pxs)  # shape: (15, 15), (15, 15)
# `grid_x` and `grid_y` map /all/ integer PCS coordinates. We only need the
# locations that actually correspond to a valve.
valve2px_x = _np.reshape(_grid_x, -1)[1::2]  # shape: (112,)
valve2px_y = _np.reshape(_grid_y, -1)[1::2]  # shape: (112,)

# Tidy up the namespace
del _pxs, _grid_x, _grid_y
del _os, _np

# ------------------------------------------------------------------------------
#  create_header_string
# ------------------------------------------------------------------------------


def create_header_string() -> str:
    w = 20
    header_str = (
        f"{'TYPE':<{w}}OpenSimplex noise v{__version__}\n"
        f"{'DATE':<{w}}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"{'N_FRAMES':<{w}}{N_FRAMES}\n"
        f"{'DT_FRAME':<{w}}{DT_FRAME} s\n\n"
        f"{'BW_THRESHOLD':<{w}}{BW_THRESHOLD}\n"
        f"{'TARGET_TRANSPARENCY':<{w}}{TARGET_TRANSPARENCY}\n\n"
        f"{'FEATURE_SIZE_A':<{w}}{FEATURE_SIZE_A}\n"
        f"{'FEATURE_SIZE_B':<{w}}{FEATURE_SIZE_B}\n\n"
        f"{'T_STEP_A':<{w}}{T_STEP_A}\n"
        f"{'T_STEP_B':<{w}}{T_STEP_B}\n\n"
        f"{'SEED_A':<{w}}{SEED_A}\n"
        f"{'SEED_B':<{w}}{SEED_B}\n\n"
        f"{'MIN_VALVE_DURATION':<{w}}{MIN_VALVE_DURATION} frames\n\n"
        f"{'PCS_PIXEL_DIST':<{w}}{PCS_PIXEL_DIST}\n"
        f"{'N_PIXELS':<{w}}{N_PIXELS}\n"
        f"{'X_STEP_A':<{w}}{X_STEP_A}\n"
        f"{'X_STEP_B':<{w}}{X_STEP_B}\n\n"
    )

    return header_str
