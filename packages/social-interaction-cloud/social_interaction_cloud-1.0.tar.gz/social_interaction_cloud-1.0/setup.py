import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Includes all other files that are within your project folder
    include_package_data=True,

    # Name of your Package
    name='social_interaction_cloud',

    # Project Version
    version='1.0',

    # Description of your Package
    description='Python connectors for the Social Interaction Cloud',

    # Name of the Creator
    author='Mike Ligthart',

    # Creator's mail address
    author_email='m.e.u.ligthart@vu.nl',

    # Projects you want to include in your Package
    packages=['social_interaction_cloud'],

    # Dependencies/Other modules required for your package to work
    install_requires=['protobuf', 'redis', 'simplejson'],

    # Classifiers allow your Package to be categorized based on functionality
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)