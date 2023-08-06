import setuptools
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []  # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='simple-proxy-wysohn',
    version='0.4.3',
    description='Simple proxy library',
    long_description='Simple proxy library',
    author='wysohn',
    author_email='wysohn2002@naver.com',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
)
