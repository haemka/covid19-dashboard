from setuptools import find_packages
from setuptools import setup

setup(
    name='covinflux',
    version='0.1',
    url='https://github.com/haemka/corvid19-dashboard',
    license='',
    author='Henner M. Kruse',
    author_email='github@haemka.de',
    description='COVID-19 open data importer for InfluxDB and Grafana dashboard',
    install_requires=[
        'influxdb',
        'urllib3'
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=['src/pycovinflux'],
    data_files=[("conf", ["conf/covinflux-sample.conf"])]

)
