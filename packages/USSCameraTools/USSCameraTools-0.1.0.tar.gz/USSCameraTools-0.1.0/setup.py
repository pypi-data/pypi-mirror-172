from setuptools import setup,find_packages

setup(
    name='USSCameraTools',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/USSVision/USSCommonTools/tree/main/Packages/USSCameraTools',
    author='USS Vision',
    author_email='bhelfer@ussvision.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['wheel','opencv-python','harvesters',],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',         
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)