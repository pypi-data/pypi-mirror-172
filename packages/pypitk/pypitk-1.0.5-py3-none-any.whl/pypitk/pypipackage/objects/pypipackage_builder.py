import osiotk as os
from .. import cli as cli
from ... import constants as _constants
from .pypipackage import PYPIPackage
from .system_args import SystemArgs


def __iter_package_path_content(__package: PYPIPackage):
    for key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
        path = getattr(__package.paths, key)
        content = getattr(__package.content, key)
        yield (path, content)


def __build_package_content(__package: PYPIPackage):
    if __package.config.build.build_files:
        for (path, content) in __iter_package_path_content(__package):
            os.writes(path, content=content, is_abspath=True)
    else:
        paths = []
        for (path, content) in __iter_package_path_content(__package):
            message = f"writing content to {path}:\n\n{content}\n\n"
            paths.append(path)
            print(message)
        paths = "\n".join(paths)
        print(f"paths:\n\n{paths}")


def __process_package_installation(__package: PYPIPackage):
    config = __package.config
    if config.build.autoinstall:
        content = __package.content
        private_install_locally_command = content.private_install_locally_command
        private_install_locally_command = f"cd {config.package.parentdir}/{config.package.name};{private_install_locally_command}"
        if private_install_locally_command:
            cli.emit_process_update(f"running {private_install_locally_command}")
            os.system(private_install_locally_command)


def __mk_package_filetree(__package: PYPIPackage):
    subdir_structure = __package.config.build.subdir_structure
    parentdir = __package.config.package.parentdir
    if __package.config.build.build_files:
        os.mk_filetree(subdir_structure, parentdir=parentdir)


def build_package(__system_args: SystemArgs = None):

    package = PYPIPackage.init(system_args=__system_args)
    if package is not None:
        for build_method in (
            __mk_package_filetree,
            __build_package_content,
            __process_package_installation,
        ):
            build_method(package)
