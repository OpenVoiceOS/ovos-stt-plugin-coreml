#!/usr/bin/env python3
import os

from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-stt-plugin-coreml = ovos_stt_plugin_coreml:CoremlSTT'


BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read a requirements file, and drop the comments and the empty lines.

    The requirements are read from the file and not repeated here, so that one
    list is the only list. A hardcoded copy of this list did not name
    coremltools or numpy, both of which the package imports at module level,
    so every install of the package made an entry point that raises.
    """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=')
                            for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


def get_version():
    """ Find the version of the package"""
    version_file = f'{BASEDIR}/ovos_stt_plugin_coreml/version.py'
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


setup(
    name='ovos-stt-plugin-coreml',
    version=get_version(),
    url='https://github.com/OpenVoiceOS/ovos-stt-plugin-coreml',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_stt_plugin_coreml'],
    install_requires=required("requirements.txt"),
    extras_require={"test": required("requirements-test.txt")},
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords='apple ovos plugin stt',
    entry_points={'opm.stt': PLUGIN_ENTRY_POINT}
)
