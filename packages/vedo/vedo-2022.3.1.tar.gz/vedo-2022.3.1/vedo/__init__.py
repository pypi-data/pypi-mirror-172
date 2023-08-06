#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. include:: ../docs/documentation.md
"""
##### To generate documentation #######################################################
# cd Projects/vedo
# pip uninstall vedo
# pdoc3 --html . --force -c lunr_search="{'fuzziness': 0, 'index_docstrings': True}"
# chmod 755 html/ -R
# mount_staging
# rm ~/Projects/StagingServer/var/www/html/vtkplotter.embl.es/autodocs/html
# mv html/ ~/Projects/StagingServer/var/www/html/vtkplotter.embl.es/autodocs/
############## pdoc excludes
__pdoc__ = {}
__pdoc__['embedWindow'] = False
__pdoc__['backends'] = False
__pdoc__['cli'] = False
__pdoc__['cmaps'] = False
__pdoc__['version'] = False
__pdoc__['base.BaseActor.getPointArray'] = False
__pdoc__['base.BaseActor.getCellArray'] = False
__pdoc__['base.BaseActor.addPointArray'] = False
__pdoc__['base.BaseActor.addCellArray'] = False
__pdoc__['pointcloud.Points.pointColors'] = False
__pdoc__['pointcloud.Points.cellColors'] = False
__pdoc__['pointcloud.Points.thinPlateSpline'] = False
__pdoc__['pointcloud.Points.warpByVectors'] = False
__pdoc__['pointcloud.Points.distanceToMesh'] = False

#######################################################################################

__author__     = "Marco Musy"
__license__    = "MIT"
__maintainer__ = "M. Musy"
__email__      = "marco.musy@embl.es"
__status__     = "dev"
__website__    = "https://github.com/marcomusy/vedo"

######################################################################## imports
import os
import sys
import warnings
import logging
from deprecated import deprecated
import numpy as np
from numpy import sin, cos, sqrt, exp, log, dot, cross  # just because useful
import vtkmodules.all as vtk

#################################################
from vedo.version import _version as __version__
from vedo.utils import *
import vedo.settings as settings
from vedo.colors import *
from vedo.shapes import *
from vedo.io import *
from vedo.base import *
from vedo.ugrid import *
from vedo.assembly import *
from vedo.pointcloud import *
from vedo.mesh import *
from vedo.picture import *
from vedo.volume import *
from vedo.tetmesh import *
from vedo.shapes import *
from vedo.addons import *
from vedo.plotter import *
import vedo.applications as applications

##################################################################################
########################################################################## GLOBALS
vtk_version = [
    int(vtk.vtkVersion().GetVTKMajorVersion()),
    int(vtk.vtkVersion().GetVTKMinorVersion()),
    int(vtk.vtkVersion().GetVTKBuildVersion()),
]

try:
    import platform
    sys_platform = platform.system()
except:
    sys_platform = ""

if vtk_version[0] >= 9:
    if "Windows" in sys_platform or "Linux" in sys_platform:
        settings.useDepthPeeling = True


######################################################################### logging
class _LoggingCustomFormatter(logging.Formatter):

    logformat = "[vedo.%(filename)s:%(lineno)d] %(levelname)s: %(message)s"

    white = "\x1b[1m"
    grey = "\x1b[2m\x1b[1m\x1b[38;20m"
    yellow = "\x1b[1m\x1b[33;20m"
    red = "\x1b[1m\x1b[31;20m"
    inv_red = "\x1b[7m\x1b[1m\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey  + logformat + reset,
        logging.INFO: white + logformat + reset,
        logging.WARNING: yellow + logformat + reset,
        logging.ERROR: red + logformat + reset,
        logging.CRITICAL: inv_red + logformat + reset,
    }

    def format(self, record):
         log_fmt = self.FORMATS.get(record.levelno)
         formatter = logging.Formatter(log_fmt)
         return formatter.format(record)

logger = logging.getLogger("vedo")
_chsh = logging.StreamHandler()
_chsh.flush = sys.stdout.flush
_chsh.setLevel(logging.DEBUG)
_chsh.setFormatter(_LoggingCustomFormatter())
logger.addHandler(_chsh)
logger.setLevel(logging.INFO)

# silence annoying messages
warnings.simplefilter(action="ignore", category=FutureWarning)
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


################################################################################
installdir = os.path.dirname(__file__)
dataurl    = "https://vedo.embl.es/examples/data/"

plotter_instance = None
notebook_plotter = None
notebookBackend  = None

## fonts
fonts_path = os.path.join(installdir, "fonts/")

## a fatal error occurs when compiling to exe,
## developer needs to copy the fonts folder to the same location as the exe file to solve this problem
if not os.path.exists(fonts_path):
    fonts_path = "fonts/"

fonts = [_f.split(".")[0] for _f in os.listdir(fonts_path) if '.npz' not in _f]
fonts = list(sorted(fonts))

last_figure = None  # pyplot module
