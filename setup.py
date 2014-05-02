try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Corenlp Sentiment Only Server. Based on https://bitbucket.org/torotoki/corenlp-python',
    'author': 'Deepu T Philip',
    'url': '',
    'download_url': '',
    'author_email': 'deepu.dtp@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['corenlp_sentiment'],
    'scripts': ['bin/corenlp-sentiment-server'],
    'name': 'corenlp_sentiment'
}

setup(**config)
