from setuptools import setup

HERE = pathlib.Path(__file__).parent

setup(
    name="vidutils",
    description="OpenCV-based video prototyping tools.",
    long_description=(HERE/"README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/RiccardoLincetto/vidutils",
    author="Riccardo Lincetto",
    author_email="riccardo.lincetto@gmail.com",
    license="GNU General Public License v3.0",
    packages=["vidutils"],
    install_requires=[
        "numpy",
        "opencv-python",
        "vidsz"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
