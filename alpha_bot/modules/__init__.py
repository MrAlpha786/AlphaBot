import glob
from os.path import dirname, basename, isfile

from alpha_bot import LOGGER


def __list_modules():
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
               and f.endswith(".py")
               and not f.endswith('__init__.py')]

    return modules


MODULES = sorted(__list_modules())
LOGGER.info("modules to load: %s", str(MODULES))
__all__ = MODULES + ["MODULES"]
