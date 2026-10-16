from glob import glob
from setuptools import setup

package_name = 'robot_biztonsag'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hallgato',
    maintainer_email='hallgato@example.com',
    description='Akadalykozeli sebessegkorlatozas szimulalt robotadatokkal ROS 2-ben.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'motion_simulator = robot_biztonsag.motion_simulator:main',
            'safety_controller = robot_biztonsag.safety_controller:main',
        ],
    },
)
