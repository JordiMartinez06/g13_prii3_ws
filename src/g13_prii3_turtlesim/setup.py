import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'g13_prii3_turtlesim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jordi',
    maintainer_email='jmarric@upv.edu.es',
    description='Dibuja 13 con turtlesim',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_node = g13_prii3_turtlesim.draw_node:main',
        ],
    },
)
