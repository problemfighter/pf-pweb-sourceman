import os
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
    main_app_root = ""

    def get_python(self):
        return sys.executable

    def run_py_command(self, root, command, mode):
        command = "python " + command
        self.run_command_with_venv(root, command, mode)

    def run_setup(self, root, run_type, mode):
        setup_file_name = "setup.py"
        setup_file = os.path.join(root, setup_file_name)
        if PFPFFileUtil.is_exist(setup_file):
            command = "python " + setup_file_name + " " + run_type
            self.run_command_with_venv(root, command, mode)

    def _get_value(self, dict_data, key, default=None):
        if key in dict_data:
            return dict_data[key]
        return default

    def _run_before_start(self, yml, root_path, mode):
        if "before_start" in yml:
            console.info("Running: Before start commands")
            for command in yml["before_start"]:
                console.success(command)
                self.run_command_with_venv(command=command, root=root_path, mode=mode)

    def _run_before_end(self, yml, root_path, mode):
        if "before_end" in yml:
            console.info("Running: Before end commands")
            for command in yml["before_end"]:
                console.success(command)
                self.run_command_with_venv(command=command, root=root_path, mode=mode)

    def _process_repo_clone(self, repo, branch, lib_root):
        branch = self._get_value(repo, "branch", branch)
        self.git_repo_man.clone_or_pull_project(path=lib_root, url=repo['url'], branch=branch)

    def _run_setup_py(self, lib_root, setup_py, mode):
        if setup_py:
            self.run_setup(lib_root, setup_py, mode)

    def _resolve_lib_dependency(self, main_app_root, mode, lib_root):
        pwebsm_yml_file = os.path.join(lib_root, self.pwebsm_file_name)
        if PFPFFileUtil.is_exist(pwebsm_yml_file):
            self.process_pwebsm_file(root_path=main_app_root, mode=mode, pwebsm_yml_file=pwebsm_yml_file)

    def _run_py_script(self, py_script, root_dir, mode):
        if not py_script or not root_dir or not PFPFFileUtil.is_exist(root_dir):
            return
        console.info("Resolving  App Dependencies")
        for directory in os.listdir(root_dir):
            project_root = os.path.join(root_dir, directory)
            for command in py_script:
                if command and command.startswith('setup.py'):
                    run_type = command.replace("setup.py").strip()
                    self.run_setup(project_root, run_type, mode=mode)
                else:
                    self.run_py_command(project_root, command=command, mode=mode)

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

        run_py_script = self._get_value(dependency, "run-py-script", [])
        self._run_py_script(run_py_script, root_dir=project_root, mode=mode)

        repos = self._get_value(dependency, "repo", [])
        for repo in repos:
            if "url" not in repo:
                console.error("Invalid repo config")
                continue

            repo_name = self.git_repo_man.get_repo_name_from_url(repo['url'])
            if "name" in repo:
                repo_name = repo['name']

            lib_root = os.path.join(project_root, repo_name)
            self._process_repo_clone(repo, branch, lib_root)
            self._resolve_lib_dependency(main_app_root=main_app_root, lib_root=lib_root, mode=mode)
            self._run_setup_py(lib_root, setup_py, mode)

    def _resolve_dependencies(self, yml_object, mode, main_root):
        if not yml_object:
            return

        dependencies = []
        if "dependencies" in yml_object:
            dependencies = yml_object["dependencies"]

        for dependency in dependencies:
            self._process_dependency(mode, dependency, main_root)

    def _resolve_app_dependencies(self, yml_object, mode, main_root):
        if not yml_object:
            return

        dependencies = []
        if "app_dependencies" in yml_object:
            dependencies = yml_object["app_dependencies"]

        for dependency in dependencies:
            self._process_dependency(mode, dependency, main_root)

    def process_pwebsm_file(self, root_path, mode, pwebsm_yml_file=None):
        if not pwebsm_yml_file:
            pwebsm_yml_file = os.path.join(root_path, self.pwebsm_file_name)
        if not PFPFFileUtil.is_exist(root_path):
            console.error(self.pwebsm_file_name + " file not found!")
            return
        yml_object = YMLUtil.load_from_file(pwebsm_yml_file)
        self._run_before_start(yml_object, root_path, mode)
        self._resolve_dependencies(yml_object, mode, root_path)
        self._resolve_app_dependencies(yml_object, mode, root_path)
        self._run_before_end(yml_object, root_path, mode)

    def setup(self, repo, directory, branch, mode):
        if not directory:
            directory = self.git_repo_man.get_repo_name_from_url(repo)
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
        self.main_app_root = root_path
        self.create_virtual_env(root_path)
        self.process_pwebsm_file(root_path, mode)
        console.success("Process completed")

    def run_command_with_venv(self, root, command, mode):
        active = "source " + os.path.join(self.main_app_root, CONST.VENV_DIR, "bin", "activate")
        if sys.platform == "win32":
            active = os.path.join(self.main_app_root, CONST.VENV_DIR, "Scripts", "activate")
        command = active + " && " + command
        pcli.run(command, root, env=dict(os.environ, **{"source": mode}))

    def create_virtual_env(self, root):
        if not PFPFFileUtil.is_exist(os.path.join(root, CONST.VENV_DIR)):
            console.success("Creating virtual environment")
            pcli.run(self.get_python() + " -m venv " + CONST.VENV_DIR, root)


pm = ProjectManager()
