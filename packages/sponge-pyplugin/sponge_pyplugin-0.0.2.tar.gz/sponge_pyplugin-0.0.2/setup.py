import os
import pathlib
from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class MyInstall(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = f"{pathlib.Path(self.build_temp)}/{ext.name}"
        os.makedirs(build_temp, exist_ok=True)
        out_dir = input("input the target path for the library\n")
        out_dir = pathlib.Path(out_dir).absolute()

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(out_dir),
            "-DCMAKE_BUILD_TYPE=Release"
        ]

        build_args = ["--config Release"]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{str(cwd)}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))

setup(name="sponge_pyplugin",
      version="0.0.1",
      description="This is the python plugin of SPONGE",
      package=["sponge_pyplugin"],
      setup_requires = ["cmake"],
      ext_modules=[CMakeExtension("sponge_pyplugin")],
      cmdclass={"install": MyInstall},
      package_data={'sponge_pyplugin': ['*.cpp']},
      )