import subprocess


class PCLI:

    def run(self, command, home):
        response = subprocess.run(command, shell=True, cwd=home)
        return response


pcli = PCLI()
