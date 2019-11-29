from setuptools import setup, find_packages

setup(
    name="BorderlandTool",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blt = borderland_tool.__main__:main'
        ]
    }
)

