from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open(f'src/{name}/version.py') as f:
        for line in f:
            if line.startswith(('major', 'minor', 'patch')):
                yield line.split('=')[1].strip()


pkgs = find_packages('src')

name = pkgs[0]

setup(
    author_email='nakamaru@csg.ci.i.u-tokyo.ac.jp',
    author='Tomoki Nakamaru',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=readme(),
    name=name,
    package_dir={'': 'src'},
    packages=pkgs,
    version='.'.join(version())
)
