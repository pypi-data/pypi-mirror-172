from distutils.core import setup


long_description1 = """
                      This package contains several submodules which can be directly used after installing the package.

                      You can find the details of our package from:

                      https://github.com/Business-Brio/MIT_Open_license.git


                    """

setup(name='business_brio_package',
      packages = ['business_brio_package'],
      version='0.0.6',
      description='A package contains several submodules and functions',
      long_description= long_description1,
      url='https://github.com/Business-Brio/MIT_Open_license.git',
      download_url = 'https://github.com/Business-Brio/MIT_Open_license/archive/0.0.1.tar.gz',
      author='business_brio',
      
      keywords = ['chi_test',],
      license='MIT',

      install_requires=['pandas','numpy','scipy',],
  

      classifiers=[
        'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', # Your License Here  
        'Programming Language :: Python :: 3',    # List Python versions that you support Here  
        'Programming Language :: Python :: 3.4',
        ],
)