#! /usr/bin/env python

from __future__ import absolute_import, division, print_function

from setuptools import setup, Extension

import os, glob, numpy, subprocess, sys

PY2 = sys.version_info.major < 3
if PY2:
    MATPLOTLIB_DEP = 'matplotlib<3'
    ASTROPY_DEP = 'astropy>=1.0'
else:
    MATPLOTLIB_DEP = 'matplotlib'
    ASTROPY_DEP = 'astropy>=3.0'


def get_description():
    def get_description_lines():
        seen_desc = False
        with open('README.md', encoding='utf-8') as f:
            for line in f:
                if seen_desc:
                    if line.startswith('##'):
                        break
                    line = line.strip()
                    if line:
                        yield line
                elif line.startswith('## Features'):
                    seen_desc = True

    return ' '.join(get_description_lines())

print(get_description())


def indir(path, files):
    return [os.path.join(path, f) for f in files]


global_macros = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aipy-eovsa',
    setup_requires=['setuptools_scm'],
    version='0.1.1.3',
    description='Astronomical Interferometry in PYthon customized for EOVSA',
    # long_description=get_description(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=("LICENSE", "LICENSE-GPL"),
    author='Dale Gary, Sijie Yu',
    author_email='sijie.yu@njit.edu',
    url='https://github.com/ovro-eovsa/aipy-eovsa',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    install_requires=[
        ASTROPY_DEP,
        'healpy>=1.11',
        MATPLOTLIB_DEP,
        'numpy>=1.2',
        'ephem>=3.7.3.2',
        'scipy>=0.19',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov'
        ]
    },
    package_dir={'aipy': 'aipy', 'aipy._src': 'aipy/_src'},
    packages=['aipy', 'aipy._src'],
    ext_modules=[
        Extension('aipy._miriad', ['aipy/_miriad/miriad_wrap.cpp'] + \
                  indir('aipy/_miriad/mir', ['uvio.c', 'hio.c', 'pack.c', 'bug.c',
                                             'dio.c', 'headio.c', 'maskio.c']),
                  define_macros=global_macros,
                  include_dirs=[numpy.get_include(), 'aipy/_miriad',
                                'aipy/_miriad/mir', 'aipy/_common']),
        Extension('aipy._deconv', ['aipy/_deconv/deconv.cpp'],
                  define_macros=global_macros,
                  include_dirs=[numpy.get_include(), 'aipy/_common']),
        # Extension('aipy._img', ['aipy/_img/img.cpp'],
        #    include_dirs = [numpy.get_include()]),
        Extension('aipy._dsp', ['aipy/_dsp/dsp.c', 'aipy/_dsp/grid/grid.c'],
                  define_macros=global_macros,
                  include_dirs=[numpy.get_include(), 'aipy/_dsp', 'aipy/_dsp/grid', 'aipy/_common']),
        Extension('aipy.utils', ['aipy/utils/utils.cpp'],
                  define_macros=global_macros,
                  include_dirs=[numpy.get_include(), 'aipy/_common']),
    ],
    scripts=glob.glob('scripts/*'),

    include_package_data=True,
    zip_safe=False,
    test_suite="tests.aipy_test.TestSuite",
)
