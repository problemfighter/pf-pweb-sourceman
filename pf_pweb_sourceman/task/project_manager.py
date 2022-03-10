import os
import subprocess
import sys
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pcli import pcli
from pf_pweb_sourceman.common.constant import CONST


class ProjectManager:

    def get_python(self):
        return sys.executable

    def active_venv(self, root):
        pass

    def setup(self, repo, directory, branch, mode):
        root_path = os.path.join(os.getcwd(), directory)
        if PFPFFileUtil.is_exist(root_path):
            console.red("Path already exist. " + str(root_path))
            return
        PFPFFileUtil.create_directories(root_path)

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(sys.version)
        print(sys.platform)
        print(sys.executable)
        print(ROOT_DIR)
        print(os.path.dirname(sys.modules['__main__'].__file__))

        response = subprocess.run(sys.executable + " --version", shell=True, cwd=ROOT_DIR, check=True)
        print(response.returncode)

        cwd = os.getcwd()
        print(cwd)
        self.create_virtual_env(root_path)

    def create_virtual_env(self, root):
        pcli.run(self.get_python() + " -m venv " + CONST.VENV_DIR, root)


pm = ProjectManager()
