from setuptools import setup, find_packages

setup(
    name="kerbiancore",
    version="0.1.0",
    description="KerbianCore: Robust, secure, and scalable toolkit for mobile app development",
    author="KerbianCore Contributors",
    author_email="opensource@kerbiancore.dev",
    url="https://github.com/kerbiancore/kerbiancore",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "kerbiancore=kerbiancore.cli:main"
        ]
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown"
)