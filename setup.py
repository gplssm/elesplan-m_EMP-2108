from setuptools import find_packages, setup


setup(
    name='elesplan_m_EMP_E_2018',
    version='0.0.0-dev',
    packages=find_packages(),
    url='https://github.com/gplssm/elesplan_m_EMP_E_2018',
    author='gplssm',
    author_email='guido.plessmann@rl-institut.de',
    description='A python package for distribution grid analysis and optimization',
    install_requires = ['reegis_tools==0.0.1+git.d806b98',
                        'pandas',
                        'xlrd'],
    dependency_links = ['https://github.com/reegis/reegis_tools/archive/d806b98314d0be25d1066460c0fe0517ba912130.zip#egg=reegis_tools-0.0.1+git.d806b98'],
)