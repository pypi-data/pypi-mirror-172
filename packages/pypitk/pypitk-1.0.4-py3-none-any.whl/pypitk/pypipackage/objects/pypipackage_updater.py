import osiotk as os
from .. import cli as cli
from .. import util as _util
from ... import constants as _constants
from .pypipackage import PYPIPackage
from .paths import Paths
from .system_args import SystemArgs


def __upgrade_version(__str: str):
    print("upgrading versions:", __str)
    if "." in __str:
        try:
            components = [int(component) for component in __str.split(".", 2)]
            upgraded = False
            for (i, e) in enumerate(components):
                if e == 9:
                    if i > 0:
                        components[i] = 0
                        components[i - 1] += 1
                        upgraded = True

            if not upgraded:
                components[-1] += 1
                upgraded = True

            result = ".".join(str(component) for component in components)
            if result == __str:
                print("error: unable to upgrade package version")
                result = None
        except BaseException as error:
            print(error)
            result = None
    else:
        result = None
    return result


def load_package(__packagedir: str) -> PYPIPackage:
    name = os.basename(__packagedir)
    paths = Paths.init(parentdir=__packagedir, package_name=name)
    return PYPIPackage.init(None, existing_config_path=paths.pypitk_config)


def update_package(
    __system_args: SystemArgs = None,
    package: PYPIPackage = None,
    packagedir: str = None,
):
    if package is None:
        if __system_args is not None:
            _packagedir = __system_args.get("packagedir", None)
            if _packagedir is not None:
                packagedir = _packagedir.value
            if packagedir is not None:
                package = load_package(packagedir)
    if package is not None:
        version = package.config.package.version
        name = _util.format_package_name(package.config.package.name)
        package.config.package.name = name
        package.config.package.parentdir = _util.format_package_path(
            name, package.config.package.parentdir
        )
        new_version = __upgrade_version(version)
        if new_version is not None:
            for key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
                path = getattr(package.paths, key)
                path = _util.format_package_path(name, path)
                content: str = getattr(package.content, key)
                content = content.replace(version, new_version)
                os.writes(path, content=content, is_abspath=True)
            message = "updated package"
        else:
            message = "unable to update package: new_version is None"
    else:
        message = "unable to update package: package is None"

    print(message)
