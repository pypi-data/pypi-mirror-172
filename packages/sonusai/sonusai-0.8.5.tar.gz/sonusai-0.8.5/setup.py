# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sonusai',
 'sonusai.data_generator',
 'sonusai.metrics',
 'sonusai.mixture',
 'sonusai.queries',
 'sonusai.utils']

package_data = \
{'': ['*'], 'sonusai': ['data/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'docopt>=0.6,<0.7',
 'h5py>=2.10.0,<2.11.0',
 'keras-tuner>=1.1.3,<2.0.0',
 'matplotlib>=3.5,<4.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pandas>=1,<2',
 'protobuf>=3.20.1,<4.0.0',
 'pyaaware>=1.3.20,<2.0.0',
 'scikit-learn>=1.0.0,<1.1.0',
 'sh>=1.14.2,<2.0.0',
 'sklearn>=0.0,<0.1',
 'sox>=1,<2',
 'tensorflow>=2.4.0,<2.5.0',
 'tensorflow_addons==0.12.1',
 'tf2onnx>=1,<2',
 'tqdm>=4.62,<5.0']

entry_points = \
{'console_scripts': ['aawscd_probwrite = sonusai.aawscd_probwrite:main',
                     'sonusai = sonusai.main:main']}

setup_kwargs = {
    'name': 'sonusai',
    'version': '0.8.5',
    'description': 'Framework for building deep neural network models for sound, speech, and voice AI',
    'long_description': "Sonus AI: Framework for simplified creation of deep NN models for sound, speech, and voice AI\n\nSonus AI includes functions for pre-processing training and validation data and\ncreating performance metrics reports for key types of Keras models:\n- recurrent, convolutional, or a combination (i.e. RCNNs)\n- binary, multiclass single-label, multiclass multi-label, and regresssion\n- training with data augmentations:  noise mixing, pitch and time stretch, etc.\n\nSonus AI python functions are used by:\n - Aaware Inc. sonusai executable:  Easily create train/validation data, run prediction, evaluate model performance\n - Keras model scripts:             User python scripts for keras model creation, training, and prediction. These can use sonusai-specific data but also some general useful utilities for trainining rnn-based models like CRNN's, DSCRNN's, etc. in Keras\n",
    'author': 'Chris Eddington',
    'author_email': 'chris@aaware.com',
    'maintainer': 'Chris Eddington',
    'maintainer_email': 'chris@aaware.com',
    'url': 'https://aaware.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
