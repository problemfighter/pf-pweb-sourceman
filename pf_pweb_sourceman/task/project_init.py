import os

from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.pwebsm.descriptor_const import DesConst
from pf_pweb_sourceman.pwebsm.pwebsm_resolver import PwebSMResolver
from pf_pweb_sourceman.task.project_manager import ProjectManager
from pf_py_file.pfpf_file_util import PFPFFileUtil
from pf_py_ymlenv.yml_util import YMLUtil


class ProjectInit:

    pwebsm_resolver = PwebSMResolver()
    project_manager = ProjectManager()

    def get_pf_react_source_dep(self):
        return {DesConst.url: "https://github.com/problemfighter/pf-react.git"}

    def get_pweb_source_dep(self):
        return {
            DesConst.name: "pf-flask-web",
            DesConst.url: "https://github.com/problemfighter/pf-flask-web.git"
        }

    def get_before_start(self):
        return []

    def get_before_end(self):
        return []

    def create_pwebsm_yml(self, project_root, mode, ui_type):
        pwebsm_file = self.pwebsm_resolver.get_pwebsm_file_name()
        pwebsm_file_path = os.path.join(project_root, pwebsm_file)
        PFPFFileUtil.delete_file(pwebsm_file_path)
        pwebsm_yml = {
            DesConst.before_start: self.get_before_start(),
            DesConst.before_end: self.get_before_end()
        }

        YMLUtil.write_to_file(pwebsm_file_path, pwebsm_yml)

    def process_project_root(self, project_root):
        if PFPFFileUtil.is_exist(project_root):
            raise Exception("{} Path already exist.".format(str(project_root)))
        PFPFFileUtil.create_directories(project_root)

    def init(self, name, port, directory, mode, ui_type):
        console.success("Initializing Project, Name: " + name)
        if not directory:
            directory = name
        project_root = self.pwebsm_resolver.project_root_dir(directory)

        self.process_project_root(project_root)

        console.success("Creating Dependency Resolver")
        self.create_pwebsm_yml(project_root, mode=mode, ui_type=ui_type)

        self.project_manager.create_virtual_env(project_root)

        console.success("Congratulations!! Project has been Initialized.")
        print("\n")
        console.info("---------------------------------------------------------")
        console.cyan("Go to project directory: " + directory)
        console.cyan("Run Command: python pweb_cli.py")


pi = ProjectInit()
