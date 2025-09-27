from setuptools import setup, find_packages

setup(
    name='pwnscript',
    version='2.1.0',
    packages=find_packages(),  # 自动查找子包
    description='A powerful CTF PWN utility toolkit with macro support',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='p0ach1l',
    url='https://github.com/p0ach1l/pwnscript',
    install_requires=[
        'pwntools>=4.8.0',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='pwn ctf security exploit hacking pwntools',
    project_urls={
        'Bug Reports': 'https://github.com/p0ach1l/pwnscript/issues',
        'Source': 'https://github.com/p0ach1l/pwnscript',
    },
)
