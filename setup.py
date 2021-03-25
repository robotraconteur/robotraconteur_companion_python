from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='RobotRaconteurCompanion',
    version='0.1.3',
    description='Robot Raconteur Python Companion Library',
    author='John Wason',
    author_email='wason@wasontech.com',
    url='http://robotraconteur.com',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    package_data={'RobotRaconteurCompanion.StdRobDef': [
        '*.robdef'
    ]},
    install_requires=[
        'RobotRaconteur',
        'numpy',
        'PyYAML',
        'setuptools',
        'importlib_resources'
    ],
    tests_require=['pytest'],
    extras_require={
        'test': ['pytest']
    }
)