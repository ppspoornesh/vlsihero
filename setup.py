from setuptools import setup, find_packages

setup(
    name="vlsi-hero",
    version="1.0.0",
    description="Interactive Digital Design Learning Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="VLSI Hero Team",
    author_email="team@vlsihero.com",
    url="https://github.com/yourusername/vlsi-hero",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    python_requires=">=3.11",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-SQLAlchemy>=3.1.1",
        "psycopg2-binary>=2.9.9",
        "Werkzeug>=3.0.1",
        "gunicorn>=23.0.0",
        "email-validator>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vlsi-hero=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.css", "*.js", "*.json"],
    },
)