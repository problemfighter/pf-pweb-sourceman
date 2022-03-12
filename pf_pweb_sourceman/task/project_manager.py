import os
import subprocess
import sys
from git import Repo
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pcli import pcli
from pf_pweb_sourceman.common.constant import CONST

from pf_py_ymlenv.yml_util import YMLUtil


class ProjectManager:

    def _log(self, text, log_type="message"):
        message = ">> " + str(text)
        if log_type == "error":
            console.red(message)
        else:
            console.green(message)

    def get_python(self):
        return sys.executable

    def active_venv(self, root):
        pass

    def get_repo_name_from_url(self, url: str):
        if not url:
            return None

        last_slash_index = url.rfind("/")
        last_suffix_index = url.rfind(".git")
        if last_suffix_index < 0:
            last_suffix_index = len(url)

        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise Exception("Invalid repo url {}".format(url))

        return url[last_slash_index + 1:last_suffix_index]

    def clone_project(self, path, url, branch):
        repo_name = self.get_repo_name_from_url(url)
        if not repo_name:
            raise Exception("Invalid repo")
        self._log("Cloning project: " + repo_name + ", Branch: " + branch)
        Repo.clone_from(url, branch=branch, to_path=path)

    def _get_value(self, dict_data, key, default=None):
        if key in dict_data:
            return dict_data[key]
        return default

    def _run_before_start(self, yml, root_path):
        if "before_start" in yml:
            for command in yml["before_start"]:
                print(command)

    def _run_before_end(self, yml, root_path):
        if "before_end" in yml:
            for command in yml["before_end"]:
                print(command)

    def _process_repo_clone(self, mode, repository):
        repos = self._get_value(repository, "repo", [])
        yml_mode = self._get_value(repository, "mode")
        if not yml_mode or mode not in yml_mode:
            self._log("There is no mode found", "error")
            return

        branch = self._get_value(repository, "branch")
        if not branch:
            raise Exception("Branch not found")

        for repo in repos:
            print(repo)

    def _process_dependency(self, mode, dependency, main_root, project_root):
        target_dir = main_root
        if "dir" in dependency:
            target_dir = os.path.join(target_dir, dependency["dir"])
        setup_py = self._get_value(dependency, "setup-py")
        git_clone = self._get_value(dependency, "git-clone")
        if not git_clone:
            return
        for repository in git_clone:
            self._process_repo_clone(mode, repository)

        print(target_dir)

    def _resolve_dependencies(self, yml_object, mode, main_root, project_root=None):
        if not yml_object:
            return

        dependencies = []
        if "dependencies" in yml_object:
            dependencies = yml_object["dependencies"]

        for dependency in dependencies:
            self._process_dependency(mode, dependency, main_root, project_root)

    def process_pwebsm_file(self, root_path, mode):
        yml_object = YMLUtil.load_from_file("D:\pfbl\guard-watch\dev-dependencies\pf-pweb-sourceman\example\pwebsm.yml")
        self._run_before_start(yml_object, root_path)
        self._resolve_dependencies(yml_object, mode, root_path)
        self._run_before_end(yml_object, root_path)

    def setup(self, repo, directory, branch, mode):
        root_path = os.path.join(os.getcwd(), directory)

        self.process_pwebsm_file(root_path, mode)

        if PFPFFileUtil.is_exist(root_path):
            self._log("Path already exist. " + str(root_path), "error")
            return
        # PFPFFileUtil.create_directories(root_path)

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
        self.clone_project(root_path, repo, branch)
        self.create_virtual_env(root_path)

    def run_setup(self, root, run_type):
        setup_file_name = "setup.py"
        setup_file = os.path.join(root, setup_file_name)
        if PFPFFileUtil.is_exist(setup_file):
            command = "python " + setup_file_name + run_type
            self.run_command_with_venv(root, command)

    def run_command_with_venv(self, root, command):
        active = "source " + os.path.join(CONST.VENV_DIR, "bin", "active")
        if sys.platform == "win32":
            active = os.path.join(CONST.VENV_DIR, "Scripts", "active")
        command = active + " && " + command
        pcli.run(command, root)


    def create_virtual_env(self, root):
        pcli.run(self.get_python() + " -m venv " + CONST.VENV_DIR, root)


pm = ProjectManager()
