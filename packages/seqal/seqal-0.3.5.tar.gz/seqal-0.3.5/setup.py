# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqal', 'seqal.samplers', 'seqal.stoppers']

package_data = \
{'': ['*']}

install_requires = \
['flair==0.10',
 'scipy>=1.8.0,<2.0.0',
 'spacy>=3.4.1,<4.0.0',
 'torch>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'seqal',
    'version': '0.3.5',
    'description': 'Sequence labeling active learning framework for Python',
    'long_description': '# SeqAL\n\n<!-- <p align="center">\n  <a href="https://codecov.io/gh/BrambleXu/seqal">\n    <img src="https://img.shields.io/codecov/c/github/BrambleXu/seqal.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p> -->\n<p align="center">\n  <a href="https://tech-sketch.github.io/SeqAL/">\n    <img src="https://github.com/tech-sketch/SeqAL/actions/workflows/mkdocs-deployment.yml/badge.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://github.com/BrambleXu/seqal/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/BrambleXu/seqal/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/seqal/">\n    <img src="https://img.shields.io/pypi/v/seqal.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/seqal.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/seqal.svg?style=flat-square" alt="License">\n</p>\n\nSeqAL is a sequence labeling active learning framework based on Flair.\n\n## Installation\n\nSeqAL is available on PyPI:\n\n`pip install seqal`\n\nSeqAL officially supports Python 3.8+.\n\n## Usage\n\nTo understand what SeqAL can do, we first introduce the pool-based active learning cycle.\n\n![al_cycle](./docs/images/al_cycle.png)\n\n- Step 0: Prepare seed data (a small number of labeled data used for training)\n- Step 1: Train the model with seed data\n  - Step 2: Predict unlabeled data with the trained model\n  - Step 3: Query informative samples based on predictions\n  - Step 4: Annotator (Oracle) annotate the selected samples\n  - Step 5: Input the new labeled samples to labeled dataset\n  - Step 6: Retrain model\n- Repeat step2~step6 until the f1 score of the model beyond the threshold or annotation budget is no left\n\nSeqAL can cover all steps except step 0 and step 4. Because there is no 3rd part annotation tool, we can run below script to simulate the active learning cycle.\n\n```\n$python examples/run_al_cycle.py --text_column 0  --tag_column 1 --data_folder ./data/sample_bio --train_file train_seed.txt --dev_file dev.txt --test_file test.txt --pool_file labeled_data_pool.txt --tag_type ner --hidden_size 256 --embeddings glove --use_rnn False --max_epochs 1 --mini_batch_size 32 --learning_rate 0.1 --sampler MaxNormLogProbSampler --query_number 2 --token_based False --iterations 5 --research_mode True\n```\n\nWe set `research_mode=True`. This means that we simulate the active learning cycle. You can also find the script in `examples/run_al_cycle.py` or `examples/active_learning_cycle_research_mode.py`. If you want to connect SeqAL with an annotation tool, you can see the script in `examples/active_learning_cycle_annotation_mode.py`.\n\nYou can find more explanations about the parameters in the following tutorials.\n\n## Tutorials\n\nWe provide a set of quick tutorials to get you started with the library. \n\n- [Tutorials on Github Page](https://tech-sketch.github.io/SeqAL/)\n- [Tutorials on Markown](./docs/)\n  - [Tutorial 1: Introduction](./docs/TUTORIAL_1_Introduction.md)\n  - [Tutorial 2: Prepare Corpus](./docs/TUTORIAL_2_Prepare_Corpus.md)\n  - [Tutorial 3: Active Learner Setup](./docs/TUTORIAL_3_Active_Learner_Setup.md)\n  - [Tutorial 4: Prepare Data Pool](./docs/TUTORIAL_4_Prepare_Data_Pool.md)\n  - [Tutorial 5: Research and Annotation Mode](./docs/TUTORIAL_5_Research_and_Annotation_Mode.md)\n  - [Tutorial 6: Query Setup](./docs/TUTORIAL_6_Query_Setup.md)\n  - [Tutorial 7: Annotated Data](./docs/TUTORIAL_7_Annotated_Data.md)\n  - [Tutorial 8: Stopper](./docs/TUTORIAL_8_Stopper.md)\n  - [Tutorial 9: Output Labeled Data](./docs/TUTORIAL_9_Output_Labeled_Data.md)\n  - [Tutorial 10: Performance Recorder](./docs/TUTORIAL_10_Performance_Recorder.md)\n  - [Tutorial 11: Multiple Language Support](./docs/TUTORIAL_11_Multiple_Language_Support.md)\n\n## Performance\n\nActive learning algorithms achieve 97% performance of the best deep model trained on full data using only 30% of the training data on the CoNLL 2003 English dataset. The CPU model can decrease the time cost greatly only sacrificing a little performance.\n\nSee [performance](./docs/performance.md) for more detail about performance and time cost.\n\n\n## Contributing\n\nIf you have suggestions for how SeqAL could be improved, or want to report a bug, open an issue! We\'d love all and any contributions.\n\nFor more, check out the [Contributing Guide](./CONTRIBUTING.md).\n\n## Credits\n\n- [Cookiecutter](https://github.com/audreyr/cookiecutter)\n- [browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\n- [flairNLP/flair](https://github.com/flairNLP/flair)\n- [modal](https://github.com/modAL-python/modAL)\n',
    'author': 'Xu Liang',
    'author_email': 'liangxu006@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BrambleXu/seqal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
