#!/usr/bin/env python


# from distutils.core import setup
# from distutils.extension import Extension
# from distutils.sysconfig import get_python_lib
from setuptools import find_packages
from setuptools import setup
from setuptools import Extension
import numpy
import os
import sys

from Cython.Build import cythonize
# from Cython.Distutils import build_ext
import pkgconfig


def pc_info(pkg):
    """
    Obtain build options for a library from pkg-config and return a dict
    that can be expanded into the argument list for Extension.
    """

    sys.stdout.write('checking for library %s... ' % pkg)

    # pkg not found
    if not pkgconfig.exists(pkg):
        sys.stdout.write('not found\n')
        sys.stderr.write('Could not find required library "%s".\n' % pkg)
        sys.exit(1)

    # get infos about the pkg
    pkg_info = pkgconfig.parse(pkg)
    info = {
        'define_macros': pkg_info['define_macros'],
        'include_dirs': pkg_info['include_dirs'],
        'libraries': pkg_info['libraries'],
        'library_dirs': pkg_info['library_dirs'],
    }
    sys.stdout.write('ok\n')
    #sys.stdout.write('- cflags: %s\n' % cflags)
    #sys.stdout.write('- libs: %s\n' % libs)

    return info


def combine_info(*args):
    """ Combine multiple result dicts from L{pc_info} into one. """

    # init
    info = {
        'define_macros': [],
        'include_dirs': [],
        'libraries': [],
        'library_dirs': [],
    }

    # fill
    for a in args:
        info['define_macros'].extend(a.get('define_macros', []))
        info['include_dirs'].extend(a.get('include_dirs', []))
        info['libraries'].extend(a.get('libraries', []))
        info['library_dirs'].extend(a.get('library_dirs', []))

    return info


# Readme
readme_filepath = os.path.join(os.path.dirname(__file__), "README.md")
try:
    import pypandoc
    long_description = pypandoc.convert(readme_filepath, 'rst')
except ImportError:
    long_description = open(readme_filepath).read()


# find dependencies
try:
    gl_info = pc_info('gl')
    print("*************")
    print(gl_info)
    print("*************")
except SystemExit:
    # OSX: work around to include opengl.framework during compilation
    os.environ['LDFLAGS'] = '-framework opengl -framework Cocoa'
    os.environ['CFLAGS'] = '-framework opengl -framework Cocoa'
    gl_info = {
        'define_macros': [],
        'include_dirs': [],
        'libraries': [],
        'library_dirs': [],
    }
numpy_info = {'include_dirs': [numpy.get_include()]}


# sources
ext_sources = [
    'src/cmgl/cmgl.pyx',
]

# extension
ext = Extension(
    name='cmgl.cmgl',
    sources=ext_sources,
    **combine_info(
        gl_info,
        numpy_info
    )
)

# setup
setup(
    name='cmgl',
    version='1.0',
    description='CMGL is a Python binding for OpenGL in Cython that uses context managers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='FoFiX team',
    author_email='fofix@perdu.fr',
    license='GPLv2+',
    url='https://github.com/fofix/python-cmgl',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='opengl',
    ext_modules=cythonize(ext, compiler_directives={'language_level': sys.version_info[0]}),
    setup_requires=['cython', 'numpy', 'pytest-runner'],
    install_requires=[
        'Cython >= 0.27',
        'numpy >= 1.13',
        'pkgconfig >= 1.5',
    ],
    test_suite="tests",
    tests_require=['PyOpenGL', 'pytest'],
)
