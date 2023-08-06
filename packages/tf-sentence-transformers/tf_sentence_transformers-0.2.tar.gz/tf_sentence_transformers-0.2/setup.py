from setuptools import setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="tf_sentence_transformers",
    version="0.2",
    description="A Tensorflow SentenceTransformer layer that takes in strings as input.",
    url="https://github.com/zzsi/tf_sentence_transformers",
    author="ZZ Si",
    author_email="zhangzhang.si@gmail.com",
    license="MIT",
    packages=["tf_sentence_transformers"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
