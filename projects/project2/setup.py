from dotenv import load_dotenv
load_dotenv()

from setuptools import find_packages, setup

setup(
    name='flack',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'flask_sqlalchemy',
        'python-dotenv'
    ],
)