from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='RobotRaconteurCompanion',
    version='0.3.0',
    description='Robot Raconteur Python Companion Library',
    author='John Wason',
    author_email='wason@wasontech.com',
    url='https://github.com/robotraconteur/robotraconteur_companion_python',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    package_data={'RobotRaconteurCompanion.StdRobDef': [
        '*.robdef'
    ]},
    install_requires=[
        'RobotRaconteur>=0.18.0',
        'numpy',
        'PyYAML',
        'setuptools',
        'importlib_resources',
        'general_robotics_toolbox>=0.7.1'
    ],
    tests_require=['pytest'],
    extras_require={
        'test': ['pytest']
    }
)