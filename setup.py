#!/usr/bin/env python


# from distutils.core import setup
# from distutils.extension import Extension
# from distutils.sysconfig import get_python_lib
from setuptools import setup
from setuptools import Extension
import numpy
import os
import shlex
import subprocess
import sys

from Cython.Build import cythonize
# from Cython.Distutils import build_ext


def find_command(cmd):
    """ Find a program on the PATH, or, on win32, in the dependency pack. """

    sys.stdout.write('checking for program %s... ' % cmd)

    if os.name == 'nt':
        # search in the deppack
        path = os.path.join('.', 'win32', 'deps', 'bin', cmd + '.exe')
    else:
        # search in the path
        # TODO: replace 'dir' var
        path = None
        for dir in os.environ['PATH'].split(os.pathsep):
            if os.access(os.path.join(dir, cmd), os.X_OK):
                path = os.path.join(dir, cmd)
                break

    # cmd not found
    if path is None or not os.path.isfile(path):
        sys.stdout.write('not found\n')
        sys.stderr.write('Could not find required program "%s".\n' % cmd)
        sys.exit(1)

    # print the found path
    sys.stdout.write('%s\n' % path)

    return path


def def_split(x):
    """ Pick out anything interesting in the cflags and libs, and silently drop
    the rest. """

    pair = list(x.split('=', 1))
    if len(pair) == 1:
        pair.append(None)

    return tuple(pair)


def pc_exists(pkg):
    """ Check whether pkg-config thinks a library exists. """

    return os.spawnl(os.P_WAIT, pkg_config, 'pkg-config', '--exists', pkg) == 0


def pc_info(pkg):
    """
    Obtain build options for a library from pkg-config and return a dict
    that can be expanded into the argument list for Extension.
    """

    sys.stdout.write('checking for library %s... ' % pkg)

    # pkg not found
    if not pc_exists(pkg):
        sys.stdout.write('not found')
        sys.stderr.write('Could not find required library "%s".\n' % pkg)
        sys.exit(1)

    # get flags and libs
    cflags = shlex.split(subprocess.check_output([pkg_config, '--cflags', pkg]).decode())
    libs = shlex.split(subprocess.check_output([pkg_config, '--libs', pkg]).decode())

    # get infos about the pkg
    info = {
        'define_macros': [def_split(x[2:]) for x in cflags if x[:2] == '-D'],
        'include_dirs': [x[2:] for x in cflags if x[:2] == '-I'],
        'libraries': [x[2:] for x in libs if x[:2] == '-l'],
        'library_dirs': [x[2:] for x in libs if x[:2] == '-L'],
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


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()


# find pkg-config so we can find the libraries we need.
pkg_config = find_command('pkg-config')

# find dependencies
try:
    gl_info = pc_info('gl')
except SystemExit:
    gl_info = {
        'define_macros': [],
        'include_dirs': [],
        'libraries': [],
        'library_dirs': [],
    }
numpy_info = {'include_dirs': [numpy.get_include()]}


# sources
ext_sources = [
    'cmgl/cmgl.pyx'
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
    packages=['cmgl'],
    package_data={'cmgl': ['*.dll']},
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
    ],
    test_suite="tests",
    tests_require=['PyOpenGL', 'pytest'],
)
