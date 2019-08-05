import setuptools

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name='sudoku-solver',
    version='0.1.0',
    author='Robert Lucian Chiriac',
    author_email='robert.lucian.chiriac@gmail.com',
    description='A Python CLI tool to solve a sudoku board by using simulated annealing',
    url='https://github.com/RobertLucian/sudoku-simulated-annealing',
    py_modules=['sudokus'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    entry_points='''
        [console_scripts]
        sasudoku=sudoku:main
    '''
)