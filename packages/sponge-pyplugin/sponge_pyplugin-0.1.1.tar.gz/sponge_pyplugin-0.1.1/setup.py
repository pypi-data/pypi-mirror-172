import sys
import os
import pathlib
from setuptools import setup, Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.egg_info import egg_info

class MyInstall(install):
    def run(self):
        self.run_command('build_ext')

class MyBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = f"{pathlib.Path(self.build_temp)}/{ext.name}"
        os.makedirs(build_temp, exist_ok=True)
        for i, argv in enumerate(sys.argv):
            if argv == "--root":
                out_dir = pathlib.Path(sys.argv[i+1])
                break
        else:
            raise ValueError("root should be provided. Use '--root absolute_path' to set the root path")
        if not out_dir.is_absolute():
            raise ValueError("root should be an absolute path")

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
      version="0.1.1",
      description="This is the python plugin of SPONGE",
      ext_modules=[Extension("sponge_pyplugin", [])],
      cmdclass={"install": MyInstall, "bdist_wheel": MyInstall, "build_ext":MyBuildExt, "egg_info": MyEggInfo},
      data_files=[("cpp", "*.cpp")]
      )