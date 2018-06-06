from setuptools import find_packages, setup


setup(
    name='elesplan_m_EMP_E_2018',
    version='0.0.0-dev',
    packages=find_packages(),
    url='https://github.com/gplssm/elesplan_m_EMP_E_2018',
    author='gplssm',
    author_email='guido.plessmann@rl-institut.de',
    description='A python package for distribution grid analysis and optimization',
    install_requires=[
        'pandas',
        'oemof==0.2.2dev+git.86f3b64',
        'xlrd'],
    dependency_links=['https://github.com/oemof/oemof/archive/86f3b6431b8f31794700ae2669abaa670a1f76a3.zip#egg=oemof-0.2.2dev+git.86f3b64'],
    entry_points={
        'console_scripts': [
            'elesplan_m = elesplan_m_EMP_E_2018.elesplan_m:elesplan_m_cmd']
        }
)