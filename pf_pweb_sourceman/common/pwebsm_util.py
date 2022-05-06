import os


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
    def get_template_react_dir():
        return os.path.join(PwebSMUtil.get_template_dir(), "react")
