#!/usr/bin/env python3

import sys
import os
import subprocess
import pkg_resources

def check_virtualenv():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Running inside a virtual environment.")
    else:
        raise RuntimeError("This script must be run inside a virtual environment.")

def install_packages():
    packages = [
        "beautifulsoup4",
        "pytest"
    ]
    
    #установка пак-в через subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)

def list_installed_packages():
    installed_packages = pkg_resources.working_set
    packages_list = sorted(["{}=={}".format(i.key, i.version) for i in installed_packages])
    return packages_list

def save_requirements(packages_list):
    with open("requirements.txt", "w") as f:
        for line in packages_list:
            f.write(line + "\n")

def main():
    check_virtualenv()
    install_packages()
    packages_list = list_installed_packages()
    for pkg in packages_list:
        print(pkg)
    save_requirements(packages_list)

if __name__ == "__main__":
    main()

#заархивировать: zip -r lemonkyl.zip lemonkyl
#проверить список уст. библиотек: pip list