# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlhappy',
 'nlhappy.algorithms',
 'nlhappy.callbacks',
 'nlhappy.components',
 'nlhappy.configs',
 'nlhappy.datamodules',
 'nlhappy.layers',
 'nlhappy.layers.attention',
 'nlhappy.layers.classifier',
 'nlhappy.layers.embedding',
 'nlhappy.metrics',
 'nlhappy.models',
 'nlhappy.models.entity_extraction',
 'nlhappy.models.event_extraction',
 'nlhappy.models.prompt_relation_extraction',
 'nlhappy.models.prompt_span_extraction',
 'nlhappy.models.relation_extraction',
 'nlhappy.models.span_extraction',
 'nlhappy.models.text_classification',
 'nlhappy.models.text_multi_classification',
 'nlhappy.models.text_pair_classification',
 'nlhappy.models.text_pair_regression',
 'nlhappy.models.token_classification',
 'nlhappy.tricks',
 'nlhappy.utils']

package_data = \
{'': ['*'],
 'nlhappy.configs': ['callbacks/*',
                     'datamodule/*',
                     'log_dir/*',
                     'logger/*',
                     'model/*',
                     'trainer/*']}

install_requires = \
['datasets>=2.0.0',
 'googletrans==4.0.0rc1',
 'hydra-colorlog>=1.1.0',
 'hydra-core==1.1',
 'pytorch-lightning==1.7.7',
 'rich>=12.4.3,<13.0.0',
 'torch>=1.11.0',
 'transformers>=4.17.0']

extras_require = \
{':extra == "spacy" or extra == "all"': ['spacy>=3.3.0'],
 ':extra == "wandb" or extra == "all"': ['wandb>=0.12.18']}

entry_points = \
{'console_scripts': ['nlhappy = nlhappy.run:train'],
 'spacy_factories': ['span_classifier = nlhappy.components:get_spancat']}

setup_kwargs = {
    'name': 'nlhappy',
    'version': '2022.10.20',
    'description': '自然语言处理(NLP)',
    'long_description': '\n<div align=\'center\'>\n\n# NLHappy\n<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>\n<a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>\n<a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>\n<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>\n<a href="https://spacy.io/"><img alt="Spacy" src="https://img.shields.io/badge/component-%20Spacy-blue"></a>\n<a href="https://wandb.ai/"><img alt="WanDB" src="https://img.shields.io/badge/Log-WanDB-brightgreen"></a>\n</div>\n<br><br>\n\n## 📌&nbsp;&nbsp; 简介\n\nnlhappy是一款集成了数据处理,模型训练,文本处理流程构建等各种功能的自然语言处理库,并且内置了各种任务的SOTA方案,相信通过nlhappy可以让你更愉悦的做各种nlp任务\n> 它主要的依赖有\n- [pytorch-lightning](https://pytorch-lightning.readthedocs.io/en/latest/): 用于模型的训练\n- [transformers](https://huggingface.co/docs/transformers/index): 获取预训练模型\n- [datasets](https://huggingface.co/docs/datasets/index): 构建数据集\n- [spacy](https://spacy.io/usage): 用于自然语言处理流程和组件构建\n\n\n## 🚀&nbsp;&nbsp; 安装\n<details>\n<summary><b>安装nlhappy</b></summary>\n\n> 推荐先去[pytorch官网](https://pytorch.org/get-started/locally/)安装pytorch和对应cuda\n```bash\n# pip 安装\npip install --upgrade pip\npip install --upgrade nlhappy\n```\n</details>\n\n<details>\n<summary><b>其他可选</b></summary>\n\n> 推荐安装wandb用于可视化训练日志\n- 注册: https://wandb.ai/\n- 获取认证: https://wandb.ai/authorize\n- 登陆:\n```bash\nwandb login\n```\n模型训练开始后去[官网](https://wandb.ai/)查看训练实况\n</details>\n\n\n\n\n## ⚡&nbsp;&nbsp; 快速开始\n\n> 任务示例的数据集获取:[CBLUE官网](https://tianchi.aliyun.com/dataset/dataDetail?dataId=95414)\n\n<details>\n<summary><b>文本分类</b></summary>\n\n> 制作数据集\n```python\nfrom nlhappy.datamodules import TextClassificationDataModule\nfrom nlhappy.utils.make_dataset import DatasetDict, Dataset\nimport srsly\n\n# CBLUE短文本分类数据集CHIP-CTC为例\n\n# 查看数据集格式\nexample = TextClassificationDataModule.show_one_example()\n# example : {\'label\': \'新闻\', \'text\': \'怎么给这个图片添加超级链接呢？\'}\n\n# 制作数据集\ntrain_data = list(srsly.read_json(\'assets/CHIP-CTC/CHIP-CTC_train.json\'))\nval_data = list(srsly.read_json(\'assets/CHIP-CTC/CHIP-CTC_dev.json\'))\ndef convert_to_dataset(data):\n    dataset = {\'text\':[], \'label\':[]}\n    for d in data:\n        dataset[\'text\'].append(d[\'text\'])\n        dataset[\'label\'].append(d[\'label\'])\n    return Dataset.from_dict(dataset)\ntrain_ds = convert_to_dataset(train_data)\nval_ds = convert_to_dataset(val_data)\ndataset_dict = DatasetDict({\'train\':train_ds, \'validation\':val_ds})\n\n# 保存数据集, datasets为nlhappy默认数据集路径\ndataset_dict.save_to_disk(\'./datasets/CHIP-CTC\')\n```\n> 训练模型\n\n- 命令行或bash脚本,方便快捷\n```\nnlhappy \\\ndatamodule=text_classification \\\ndatamodule.dataset=TNEWS \\\n# huffingface的预训练模型都会支持\ndatamodule.plm=hfl/chinese-roberta-wwm-ext \\ \ndatamodule.batch_size=32 \\\nmodel=bert_tc \\\nmodel.lr=3e-5 \\\nseed=1234 \\\ntrainer=default\n# 默认为单gpu 0号显卡训练,可以通过以下方式修改显卡\n# trainer.devices=[1]\n# 单卡半精度训练\n# trainer.precision=16\n# 使用wandb记录日志\n# logger=wandb\n# 多卡训练\n# trainer=ddp trainer.devices=4\n```\n\n> 模型预测\n```python\nfrom nlhappy.models import BertTextClassification\n# 加载训练的checkpoint\nckpt = \'logs/path/***.ckpt\'\nmodel = BertTextClassification.load_from_ckeckpoint(ckpt)\ntext = \'研究开始前30天内，接受过其他临床方案治疗；\'\nscores = model.predict(text=text, device=\'cpu\')\n# 转为onnx模型\nmodel.to_onnx(\'path/tc.onnx\')\nmodel.tokenizer.save_pretrained(\'path/tokenizer\')\n```\n</details>\n\n<details>\n<summary><b>实体抽取</b></summary>\n\nnlhappy支持正常,嵌套和非连续的实体抽取任务,下面以可以解决嵌套任务的模型globalpointer为例\n> 制作数据集\n```python\n# CBLUE实体识别数据集CMeEE\nfrom nlhappy.datamodules import EntityExtractionDataModule\nfrom nlhappy.models.entity_extraction import GlobalPointerForEntityExtraction\nfrom nlhappy.utils.make_dataset import Dataset, DatasetDict\nimport srsly\n\n#查看数据集格式\nexample = EntityExtractionDataModule.show_one_example()\n# example : {"text":"这是一个长颈鹿","entities":[{"indexes":[4,5,6],"label":"动物", "text":"长颈鹿"}]}\n\n# 根据格式制作数据集\ntrain_data = list(srsly.read_json(\'assets/CMeEE/CMeEE_train.json\'))\nval_data = list(srsly.read_json(\'assets/CMeEE/CMeEE_dev.json\'))\ndef convert_to_dataset(data):\n    ds = {\'text\':[],\'entities\':[]}\n    for d in data:\n        ents = []\n        ds[\'text\'].append(d[\'text\'])\n        for e in d[\'entities\']:\n            if len(e[\'entity\'])>0:\n                ent = {}\n                ent[\'text\'] = e[\'entity\']\n                ent[\'indexes\'] = [idx for idx in range(len(e[\'entity\']))]\n                ent[\'text\'] = e[\'entity\']\n                ent[\'label\'] = e[\'type\']\n                ents.append(ent)\n        ds[\'entities\'].append(ents)\n    return Dataset.from_dict(ds) \ntrain_ds = convert_to_dataset(train_data)\nval_ds = convert_to_dataset(val_data)\ndataset_dict = DatasetDict({\'train\':train_ds, \'validation\':val_ds})\ndataset_dict.save_to_disk(\'./datasets/CMeEE\')\n\n\n```\n> 训练模型\n\n- 编写训练脚本\n```bash\nnlhappy \\\ndatamodule=entity_extraction \\\ndatamodule.dataset=CMeEE \\\ndatamodule.plm=hfl/chinese-roberta-wwm-ext \\\ndatamodule.batch_size=16 \\\nmodel=globalpointer \\\nmodel.lr=3e-5 \\\nseed=123\n# 默认trainer为单卡训练\ntrainer=default\n\n# 多卡\n# trainer=ddp \\\n# trainer.devices=4 \\\n# trainer.precision=16 #半精度\n\n# 如果安装了wandb则可以使用wandb\n# logger=wandb \n```\n\n> 模型推理\n\n```python\nfrom nlhappy.models import GlobalPointer\nckpt = \'logs/path/***.ckpt\'\nmodel = GlobalPointer.load_from_ckeckpoint(ckpt)\nents = model.predcit(\'文本\')\n\n# 转为onnx模型,进行后续部署\nmodel.to_onnx(\'path/tc.onnx\')\nmodel.tokenizer.save_pretrained(\'path/tokenizer\')\n```\n</details>\n\n<details>\n<summary><b>关系抽取</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>事件抽取</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>摘要</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>翻译</b></summary>\nTODO\n</details>\n\n\n## 论文复现',
    'author': 'wangmengdi',
    'author_email': '790990241@qq.om',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
