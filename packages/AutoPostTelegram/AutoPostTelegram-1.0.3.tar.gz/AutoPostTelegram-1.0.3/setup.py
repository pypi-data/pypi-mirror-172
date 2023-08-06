import setuptools


with open("README.md", "r") as txt:
    long_description = txt.read()

setuptools.setup(
    name='AutoPostTelegram',
    version='1.0.3',
    description='An Telegram Auto Post Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    author='Aasfcyberking',
    author_email='aasfvl@gmail.com',
    url='https://github.com/AasfCyberKing/AutoPostTelegram/',
    packages=setuptools.find_packages(),
    install_requires= ['requests', 'datetime'],
    python_requires='>=3.6'
)
