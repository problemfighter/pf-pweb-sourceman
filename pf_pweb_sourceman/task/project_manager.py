import os
import subprocess
import sys
from pf_pweb_sourceman.task.git_repo_man import GitRepoMan
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.common.pcli import pcli
from pf_pweb_sourceman.common.constant import CONST
from pf_py_ymlenv.yml_util import YMLUtil


class ProjectManager:
    git_repo_man = GitRepoMan()
    pwebsm_file_name = "pwebsm.yml"

    def _log(self, text, log_type="message"):
        message = ">> " + str(text)
        if log_type == "error":
            console.red(message)
        else:
            console.green(message)

    def get_python(self):
        return sys.executable

    def run_setup(self, root, run_type):
        setup_file_name = "setup.py"
        setup_file = os.path.join(root, setup_file_name)
        if PFPFFileUtil.is_exist(setup_file):
            command = "python " + setup_file_name + run_type
            self.run_command_with_venv(root, command)

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

    def _process_repo_clone(self, repo, branch, lib_root):
        branch = self._get_value(repo, "branch", branch)
        self.git_repo_man.clone_or_pull_project(path=lib_root, url=repo['url'], branch=branch)

    def _run_setup_py(self, lib_root, setup_py):
        if setup_py:
            self.run_setup(lib_root, setup_py)

    def _resolve_lib_dependency(self, main_app_root, mode, lib_root):
        pwebsm_yml_file = os.path.join(lib_root, self.pwebsm_file_name)
        if PFPFFileUtil.is_exist(pwebsm_yml_file):
            self.process_pwebsm_file(root_path=main_app_root, mode=mode, pwebsm_yml_file=pwebsm_yml_file)

    def _process_dependency(self, mode, dependency, main_app_root):
        project_root = main_app_root
        if "dir" in dependency:
            project_root = os.path.join(project_root, dependency["dir"])
        setup_py = self._get_value(dependency, "setup-py")

        yml_mode = self._get_value(dependency, "mode")
        if not yml_mode or mode not in yml_mode:
            console.error("There is no mode found")
            return

        branch = self._get_value(dependency, "branch")
        if not branch:
            console.error("Branch not found")
            return

        repos = self._get_value(dependency, "repo", [])
        for repo in repos:
            if "name" not in repo or "url" not in repo:
                console.error("Invalid repo config")
                continue
            lib_root = os.path.join(repo['name'], project_root)
            self._process_repo_clone(repo, branch, lib_root)
            self._run_setup_py(lib_root, setup_py)
            self._resolve_lib_dependency(main_app_root=main_app_root, lib_root=lib_root, mode=mode)

    def _resolve_dependencies(self, yml_object, mode, main_root):
        if not yml_object:
            return

        dependencies = []
        if "dependencies" in yml_object:
            dependencies = yml_object["dependencies"]

        for dependency in dependencies:
            self._process_dependency(mode, dependency, main_root)

    def process_pwebsm_file(self, root_path, mode, pwebsm_yml_file=None):
        if not pwebsm_yml_file:
            pwebsm_yml_file = os.path.join(root_path, self.pwebsm_file_name)
        if not PFPFFileUtil.is_exist(root_path):
            console.error(self.pwebsm_file_name + " file not found!")
            return
        yml_object = YMLUtil.load_from_file(pwebsm_yml_file)
        self._run_before_start(yml_object, root_path)
        self._resolve_dependencies(yml_object, mode, root_path)
        self._run_before_end(yml_object, root_path)

    def setup(self, repo, directory, branch, mode):
        root_path = os.path.join(os.getcwd(), directory)
        if PFPFFileUtil.is_exist(root_path):
            console.error("Path already exist. " + str(root_path))
            return
        self._setup_or_update(root_path=root_path, repo=repo, branch=branch, mode=mode)

    def update(self, mode):
        root_path = os.getcwd()
        self._setup_or_update(root_path=root_path, repo=None, branch=None, mode=mode)

    def _setup_or_update(self, root_path, repo, branch, mode):
        if repo and branch:
            self.git_repo_man.clone_or_pull_project(root_path, repo, branch)
        self.create_virtual_env(root_path)
        self.process_pwebsm_file(root_path, mode)

    def run_command_with_venv(self, root, command):
        active = "source " + os.path.join(CONST.VENV_DIR, "bin", "active")
        if sys.platform == "win32":
            active = os.path.join(CONST.VENV_DIR, "Scripts", "active")
        command = active + " && " + command
        pcli.run(command, root)

    def create_virtual_env(self, root):
        if not PFPFFileUtil.is_exist(root):
            pcli.run(self.get_python() + " -m venv " + CONST.VENV_DIR, root)


pm = ProjectManager()
