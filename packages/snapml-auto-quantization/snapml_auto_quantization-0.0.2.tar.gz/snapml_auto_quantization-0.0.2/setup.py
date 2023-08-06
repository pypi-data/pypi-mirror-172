from setuptools import setup, find_packages

version = '0.0.2'
try:
    if not os.getenv('RELEASE'):
        from datetime import date

        today = date.today()
        day = today.strftime("b%Y%m%d")
        version += day
except Exception:
    pass


setup(
    name='snapml_auto_quantization',
    version=version,
    packages=find_packages(exclude=['tests*']),
    package_dir={'snapml_auto_quantization':'snapml_auto_quantization'}, 
    package_data={
       'snapml_auto_quantization': ['snapml_auto_quantization/*.onnx', 'snapml_auto_quantization/*.obj'],
    },
    include_package_data=True,
    license='MIT',
    description='A automatic pipeline for SnapML quantization',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.sc-corp.net/Snapchat/snapml_auto_quantization',
    author='Jiazhuo Wang',
    author_email='jwang7@snapchat.com'
)
