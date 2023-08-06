import setuptools

setuptools.setup(
    name="yaadl",
    version="1.0.0",
    author="Murat Koptur",
    description="Yet Another Automatic Differentation Library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    py_modules=["autodiff"],
    package_dir={"": "."},
)
