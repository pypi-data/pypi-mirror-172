import os
import pathlib
from setuptools import setup
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class MyInstall(install):
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

class MyEggInfo(egg_info):
    def run(self):
        super().run()
        self.filelist.include("sponge_pyplugin/*")

setup(name="sponge_pyplugin",
      version="0.0.3",
      description="This is the python plugin of SPONGE",
      ext_modules=[CMakeExtension("sponge_pyplugin")],
      cmdclass={"install": MyInstall, "egg_info": MyEggInfo},
      data_files=[("cpp", "*.cpp")]
      )