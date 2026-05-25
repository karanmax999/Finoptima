"""
Setup script for Finoptima package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="finoptima",
    version="0.1.0",
    author="Finance Team",
    description="Financial Optimization & Risk Management Package - Module 1: Market Risk & Default Probability Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/finoptima",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26.0",
        "pandas>=2.0.0",
        "scipy>=1.13.0",
        "statsmodels>=0.14.0",
        "scikit-learn>=1.4.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipython>=8.20.0",
            "ipykernel>=6.29.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
)
