import setuptools

with open('README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='cassettebot',
    version='0.0.1',
    author='Karl Sims',
    author_email='author@example.com',
    description='A video maker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    scripts=['scripts/cassettebot'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)