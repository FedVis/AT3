from distutils.core import setup, Extension
module1 = Extension('m2ipy',
                    sources = ['m2ipy.c'])
setup (name = 'm2ipy',
       version = '1.0',
       description = 'm2ipy module',
       ext_modules = [module1])

