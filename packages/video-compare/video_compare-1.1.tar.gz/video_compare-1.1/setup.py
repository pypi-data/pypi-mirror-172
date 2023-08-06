from setuptools import setup

from video_compare import __version__



setup(
    name='video_compare',
    version=__version__,
    install_requires=[
        'streamlit'
    ],
    url='',
    author='Yedidya Hyams',
    author_email='yedidya.hyams@vimeo.com',
    py_modules=['video_compare'],
)