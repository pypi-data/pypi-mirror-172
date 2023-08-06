from setuptools import setup

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name="thawani",
    version="1.0.1",
    description="Thawani Python Client",
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url="https://github.com/thawani/thawani-python",
    author="Murad Lansa",
    author_email="mail@muradlansa.com",
    license="MIT",
    install_requires=["requests"],
    include_package_data=True,
    package_dir={'thawani': 'thawani', 'thawani.resources': 'thawani/resources'},
    packages=['thawani', 'thawani.resources'],
    keywords='Thawani Payment gateway Oman',

)
