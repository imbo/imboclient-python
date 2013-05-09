m distutils.core import setup

setup(
        name='imbo',
        version='0.0.1',
        author='Andreas Søvik',
        author_email='arsovik@gmail.com',
        packages=['imbo'],
        scripts=[],
        url='http://www.imbo-project.org',
        license='LICENSE.txt',
        description='Python client for Imbo',
        long_description=open('README.markdown').read(),
        install_requires=[],
)

