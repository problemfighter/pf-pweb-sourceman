from pf_pweb_sourceman.pwebsm.descriptor_const import DesConst
from pf_py_common.py_common import PyCommon


class PWebSMDescriptorCreator:

    def create(self, dependencies: list, app_dependencies: list = None, before_start: list = None, before_end: list = None):
        descriptor = {}

        if before_start:
            descriptor[DesConst.before_start] = before_start

        if app_dependencies:
            descriptor[DesConst.app_dependencies] = app_dependencies

        descriptor[DesConst.dependencies] = dependencies

        if before_end:
            descriptor[DesConst.before_end] = before_end

        return descriptor

    def create_dependency_dict(self, dir_name: str, branch: str, mode: list, repo: list = None, pyScript: list = None, setupPy: str = None, key: str = None):
        if not key:
            key = PyCommon.get_random(4).upper()

        descriptor = {
            DesConst.key: key,
            DesConst.dir: dir_name,
            DesConst.branch: branch,
            DesConst.mode: mode,
        }
        return self.edit_dependency_dict(descriptor, repo=repo, pyScript=pyScript, setupPy=setupPy)

    def add_to_existing_descriptor_before_after(self, descriptor: dict, before_start: list = None, before_end: list = None):
        if before_start:
            if DesConst.before_start not in descriptor:
                descriptor[DesConst.before_start] = before_start
            else:
                descriptor[DesConst.before_start] += before_start

        if before_end:
            if DesConst.before_end not in descriptor:
                descriptor[DesConst.before_end] = before_end
            else:
                descriptor[DesConst.before_end] += before_end
        return descriptor

    def add_to_existing_descriptor(self, descriptor: dict, dependency_name: str, dependency_key: str, mode: list = None, repo: list = None, pyScript: list = None):
        if dependency_name in descriptor:
            for dependency in descriptor[dependency_name]:
                if dependency[DesConst.key] == dependency_key:
                    self.edit_dependency_dict(dependency, repo=repo, mode=mode, pyScript=pyScript)
        return descriptor

    def add_dependency_to_existing_descriptor(self, descriptor: dict, dependency_name: str, dependencies: list):
        if dependency_name in descriptor:
            descriptor[dependency_name] += dependencies
        else:
            descriptor[dependency_name] = dependencies
        return descriptor

    def edit_dependency_dict(self, descriptor: dict, dir_name: str = None, branch: str = None, mode: list = None, repo: list = None, pyScript: list = None, setupPy: str = None):
        if dir_name:
            descriptor[DesConst.dir] = dir_name

        if branch:
            descriptor[DesConst.branch] = branch

        if mode:
            if DesConst.mode not in descriptor:
                descriptor[DesConst.mode] = mode
            else:
                descriptor[DesConst.mode] = descriptor[DesConst.mode] + mode

        if repo:
            if DesConst.repo not in descriptor:
                descriptor[DesConst.repo] = repo
            else:
                descriptor[DesConst.repo] = descriptor[DesConst.repo] + repo

        if pyScript:
            if DesConst.run_py_script not in descriptor:
                descriptor[DesConst.run_py_script] = pyScript
            else:
                descriptor[DesConst.run_py_script] = descriptor[DesConst.run_py_script] + pyScript

        if setupPy:
            descriptor[DesConst.setup_py] = setupPy

        return descriptor

    def create_repo(self, url: str, name: str = None):
        repo = {
            DesConst.url: url
        }
        if name:
            repo[DesConst.name] = name
        return repo
