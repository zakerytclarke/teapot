import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='teapotai',
    author='Zakery Clarke',
    author_email='zakerytclarke@gmail.com',
    description='Library for Teapot AI',
    keywords='llm, teapot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zakerytclarke/teapotai_lib/teapotai',
    project_urls={
        'Documentation': 'https://github.com/zakerytclarke/teapotai_lib/teapotai',
        'Bug Reports': 'https://github.com/tomchen/example_pypi_package/issues',
        'Source Code': 'https://github.com/tomchen/example_pypi_package',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch',
        'tqdm',             # for progress bars
        'transformers',     # for huggingface transformer models
        'numpy',            # for numerical operations
        'scikit-learn',     # for sklearn (cosine_similarity)
        'pydantic',         # for data validation (BaseModel)
        'regex',            # to handle regex (re is often a wrapper for regex module in modern Python)
        'langsmith'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],  # add test dependencies here
    },
)
