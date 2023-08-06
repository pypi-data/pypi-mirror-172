from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='bancodeusuarios',
    version='0.0.1',
    url='https://github.com/CaioJohnston',
    license='MIT License',
    author='Caio Johnston Soares',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='caio21070002@aluno.cesupa.br',
    keywords='Pacote',
    description='Pacote Python para cadastrar, armazenar e consultar usuários em um sistema.',
    packages=['pacotebanco'],)