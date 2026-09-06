from setuptools import find_packages, setup

package_name = 'turtle_tutorial'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ALeRT Advanced Robotics Tutorial',
    maintainer_email='noreply@example.invalid',
    description=(
        'ROS 2 example package: a turtlesim controller that drives '
        'a geometric figure without keyboard input.'
    ),
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'turtle_controller = turtle_tutorial.turtle_controller:main',
        ],
    },
)
