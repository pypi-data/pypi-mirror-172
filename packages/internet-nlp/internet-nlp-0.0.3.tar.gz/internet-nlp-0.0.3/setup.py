from setuptools import setup, find_packages
try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()


setup(
    name="internet-nlp",
    version="0.0.3",
    author="Thamognya Kodi",
    author_email="contact@thamognya.com",
    description="Allowing NLPs to connect to the internet",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="GNU Affero General Public License v3.0 or later",
    url="https://github.com/thamognya/internet-nlp",
    download_url="https://github.com/thamognya/internet-nlp",
    packages=find_packages(),
    python_requires=">=3.6.0",
    install_reqs = parse_requirements('requirements.txt', session='hack'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    keywords="Transformer NLP NLI Internet Networks BERT SOTA XLNet sentence embedding PyTorch NLP deep learning Tensorflow Huggingface"
)
