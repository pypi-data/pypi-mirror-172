# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfts', 'tfts.datasets', 'tfts.features', 'tfts.layers', 'tfts.models']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib',
 'optuna>=2.3.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'tensorflow>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'tfts',
    'version': '0.0.3',
    'description': 'Deep learning time series with TensorFlow',
    'long_description': '[license-image]: https://img.shields.io/badge/License-MIT-blue.svg\n[license-url]: https://opensource.org/licenses/MIT\n[pypi-image]: https://badge.fury.io/py/tfts.svg\n[pypi-url]: https://pypi.python.org/pypi/tfts\n[pepy-image]: https://pepy.tech/badge/tfts\n[pepy-url]: https://pepy.tech/project/tfts\n[build-image]: https://github.com/LongxingTan/Time-series-prediction/actions/workflows/test.yml/badge.svg?branch=master\n[build-url]: https://github.com/LongxingTan/Time-series-prediction/actions/workflows/test.yml?query=branch%3Amaster\n[lint-image]: https://github.com/LongxingTan/Time-series-prediction/actions/workflows/lint.yml/badge.svg?branch=master\n[lint-url]: https://github.com/LongxingTan/Time-series-prediction/actions/workflows/lint.yml?query=branch%3Amaster\n[docs-image]: https://readthedocs.org/projects/time-series-prediction/badge/?version=latest\n[docs-url]: https://time-series-prediction.readthedocs.io/en/latest/\n[coverage-image]: https://codecov.io/gh/longxingtan/Time-series-prediction/branch/master/graph/badge.svg\n[coverage-url]: https://codecov.io/github/longxingtan/Time-series-prediction?branch=master\n[codeql-image]: https://github.com/longxingtan/Time-series-prediction/actions/workflows/codeql-analysis.yml/badge.svg\n[codeql-url]: https://github.com/longxingtan/Time-series-prediction/actions/workflows/codeql-analysis.yml\n\n<h1 align="center">\n<img src="./docs/source/_static/logo.svg" width="490" align=center/>\n</h1><br>\n\n[![LICENSE][license-image]][license-url]\n[![PyPI Version][pypi-image]][pypi-url]\n[![Download][pepy-image]][pepy-url]\n[![Build Status][build-image]][build-url]\n[![Lint Status][lint-image]][lint-url]\n[![Docs Status][docs-image]][docs-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![CodeQL Status][codeql-image]][codeql-url]\n\n**[Documentation](https://time-series-prediction.readthedocs.io)** | **[Tutorials](https://time-series-prediction.readthedocs.io/en/latest/tutorials.html)** | **[Release Notes](https://time-series-prediction.readthedocs.io/en/latest/CHANGELOG.html)** | **[中文](https://github.com/LongxingTan/Time-series-prediction/blob/master/README_CN.md)**\n\n**TFTS** (TensorFlow Time Series) is a python package for time series task, supporting the classical and SOTA deep learning methods in [TensorFlow](https://www.tensorflow.org/).\n- Flexible and powerful design for time series task\n- Advanced deep learning models\n- Documentation lives at [time-series-prediction.readthedocs.io](https://time-series-prediction.readthedocs.io)\n\n## Tutorial\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1LHdbrXmQGBSQuNTsbbM5-lAk5WENWF-Q?usp=sharing)\n\n**Installation**\n\n- python >= 3.7\n- tensorflow >= 2.1\n\n``` bash\n$ pip install tfts\n```\n\n**Usage**\n\n``` python\nimport matplotlib.pyplot as plt\nimport tfts\nfrom tfts import AutoModel, KerasTrainer, Trainer\n\ntrain_length = 24\npredict_length = 8\n\n# train is a tuple of (x_train, y_train), valid is (x_valid, y_valid)\ntrain, valid = tfts.get_data(\'sine\', train_length, predict_length, test_size=0.2)\nmodel = AutoModel(\'seq2seq\', predict_length)\n\ntrainer = KerasTrainer(model)\ntrainer.train(train, valid)\n\npred = trainer.predict(valid[0])\ntrainer.plot(history=valid[0], true=valid[1], pred=pred)\nplt.show()\n```\n\n## Examples\n\n- [TFTS-prediction](./examples/run_prediction.py) for basic usage\n- [TFTS-Bert model](https://github.com/LongxingTan/KDDCup2022-Baidu) wins the **3rd place** in KDD Cup 2022 Baidu-wind power forecasting\n- [TFTS-Seq2seq model](https://github.com/LongxingTan/Data-competitions/tree/master/tianchi-enso-prediction) wins the **4th place** in Alibaba Tianchi-ENSO prediction 2021\n\n<!-- ### Performance\n\n[Time series prediction](./examples/run_prediction.py) performance is evaluated by tfts implementation, not official\n\n| Performance | [web traffic<sup>mape</sup>]() | [grocery sales<sup>rmse</sup>](https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data) | [m5 sales<sup>val</sup>]() | [ventilator<sup>val</sup>]() |\n| :-- | :-: | :-: | :-: | :-: |\n| [RNN]() | 672 | 47.7% |52.6% | 61.4% |\n| [DeepAR]() | 672 | 47.7% |52.6% | 61.4% |\n| [Seq2seq]() | 672 | 47.7% |52.6% | 61.4% |\n| [TCN]() | 672 | 47.7% |52.6% | 61.4% |\n| [WaveNet]() | 672 | 47.7% |52.6% | 61.4% |\n| [Bert]() | 672 | 47.7% |52.6% | 61.4% |\n| [Transformer]() | 672 | 47.7% |52.6% | 61.4% |\n| [Temporal-fusion-transformer]() | 672 | 47.7% |52.6% | 61.4% |\n| [Informer]() | 672 | 47.7% |52.6% | 61.4% |\n| [AutoFormer]() | 672 | 47.7% |52.6% | 61.4% |\n| [N-beats]() | 672 | 47.7% |52.6% | 61.4% |\n| [U-Net]() | 672 | 47.7% |52.6% | 61.4% |\n\n### More demos\n- [More complex prediction task](./notebooks)\n- [Time series classification](./examples/run_classification.py)\n- [Anomaly detection](./examples/run_anomaly.py)\n- [Uncertainty prediction](examples/run_uncertainty.py)\n- [Parameters tuning by optuna](examples/run_optuna_tune.py)\n- [Serving by tf-serving](./examples) -->\n\nif you prefer to use [PyTorch](https://pytorch.org/), please try [pytorch-forecasting](https://github.com/jdb78/pytorch-forecasting)\n\n## Citation\n\nIf you find tfts project useful in your research, please consider cite:\n\n```\n@misc{tfts2020,\n  author = {Longxing Tan},\n  title = {Time series prediction},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/longxingtan/time-series-prediction}},\n}\n```\n',
    'author': 'Longxing Tan',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://time-series-prediction.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
