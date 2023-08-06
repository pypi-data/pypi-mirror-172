from distutils.core import setup


def get_readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="turtle2img",
    version="1.1.5",
    description="Save turtle images as jpg or png",
    author="An-20",
    url="https://github.com/An-20/turtle2img",
    license="BSD (3 clauses)",
    long_description=get_readme(),
    packages=["turtle2img"],
    package_dir={"turtle2img": "src"},
    keywords=[
        "turtle",
        "image",
        "png",
        "jpg"
    ],
    install_requires=[
        "svglib",
        "reportlab",
        "Pillow",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
)
