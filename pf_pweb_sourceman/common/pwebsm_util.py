import os

from pf_pweb_sourceman.pwebsm.descriptor_const import DesConst
from pf_py_text.pfpt_string_util import PFPTStringUtil


class PwebSMUtil:

    @staticmethod
    def get_root_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_template_dir():
        return os.path.join(PwebSMUtil.get_root_dir(), "template")

    @staticmethod
    def get_template_common_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "common")

    @staticmethod
    def get_template_pweb_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "pweb")

    @staticmethod
    def get_template_pweb_mod_dir():
        return os.path.join(PwebSMUtil.get_template_pweb_dir(), "module")

    @staticmethod
    def get_template_react_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "react")

    @staticmethod
    def get_module_dir():
        return os.getcwd()

    @staticmethod
    def get_module_app_dir():
        return os.path.join(PwebSMUtil.get_module_dir(), DesConst.app_dependencies_dir)

    @staticmethod
    def get_module_config_dir():
        return os.path.join(PwebSMUtil.get_module_app_dir(), "config")

    @staticmethod
    def get_file_name(name):
        text = PFPTStringUtil.find_and_replace_with(name, "-", "_")
        text = PFPTStringUtil.replace_space_with(text)
        return text.lower()
