from setuptools import setup

setup(
    name='randomlib',
    version='2.5',
    # author='L3Cube',
    # author_email='l3cube.pune@gmail.com',
    description='An NLP Library for Marathi Language',
    # url='https://github.com/l3cube-pune/MarathiNLP.git',
    packages=['randomlib','randomlib.tokenizer','randomlib.preprocess','randomlib.datasets','randomlib.modelRepo','randomlib.tagger','randomlib.sentiment','randomlib.hate','randomlib.gpt'],# can also use setuptools.find_packages()
    include_package_data=True,
    install_requires=['regex','importlib.resources','pandas','transformers','numpy','torch','IPython'], 
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
