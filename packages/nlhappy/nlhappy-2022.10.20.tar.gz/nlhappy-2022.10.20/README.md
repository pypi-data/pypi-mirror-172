
<div align='center'>

# NLHappy
<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>
<a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>
<a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>
<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>
<a href="https://spacy.io/"><img alt="Spacy" src="https://img.shields.io/badge/component-%20Spacy-blue"></a>
<a href="https://wandb.ai/"><img alt="WanDB" src="https://img.shields.io/badge/Log-WanDB-brightgreen"></a>
</div>
<br><br>

## 📌&nbsp;&nbsp; 简介

nlhappy是一款集成了数据处理,模型训练,文本处理流程构建等各种功能的自然语言处理库,并且内置了各种任务的SOTA方案,相信通过nlhappy可以让你更愉悦的做各种nlp任务
> 它主要的依赖有
- [pytorch-lightning](https://pytorch-lightning.readthedocs.io/en/latest/): 用于模型的训练
- [transformers](https://huggingface.co/docs/transformers/index): 获取预训练模型
- [datasets](https://huggingface.co/docs/datasets/index): 构建数据集
- [spacy](https://spacy.io/usage): 用于自然语言处理流程和组件构建


## 🚀&nbsp;&nbsp; 安装
<details>
<summary><b>安装nlhappy</b></summary>

> 推荐先去[pytorch官网](https://pytorch.org/get-started/locally/)安装pytorch和对应cuda
```bash
# pip 安装
pip install --upgrade pip
pip install --upgrade nlhappy
```
</details>

<details>
<summary><b>其他可选</b></summary>

> 推荐安装wandb用于可视化训练日志
- 注册: https://wandb.ai/
- 获取认证: https://wandb.ai/authorize
- 登陆:
```bash
wandb login
```
模型训练开始后去[官网](https://wandb.ai/)查看训练实况
</details>




## ⚡&nbsp;&nbsp; 快速开始

> 任务示例的数据集获取:[CBLUE官网](https://tianchi.aliyun.com/dataset/dataDetail?dataId=95414)

<details>
<summary><b>文本分类</b></summary>

> 制作数据集
```python
from nlhappy.datamodules import TextClassificationDataModule
from nlhappy.utils.make_dataset import DatasetDict, Dataset
import srsly

# CBLUE短文本分类数据集CHIP-CTC为例

# 查看数据集格式
example = TextClassificationDataModule.show_one_example()
# example : {'label': '新闻', 'text': '怎么给这个图片添加超级链接呢？'}

# 制作数据集
train_data = list(srsly.read_json('assets/CHIP-CTC/CHIP-CTC_train.json'))
val_data = list(srsly.read_json('assets/CHIP-CTC/CHIP-CTC_dev.json'))
def convert_to_dataset(data):
    dataset = {'text':[], 'label':[]}
    for d in data:
        dataset['text'].append(d['text'])
        dataset['label'].append(d['label'])
    return Dataset.from_dict(dataset)
train_ds = convert_to_dataset(train_data)
val_ds = convert_to_dataset(val_data)
dataset_dict = DatasetDict({'train':train_ds, 'validation':val_ds})

# 保存数据集, datasets为nlhappy默认数据集路径
dataset_dict.save_to_disk('./datasets/CHIP-CTC')
```
> 训练模型

- 命令行或bash脚本,方便快捷
```
nlhappy \
datamodule=text_classification \
datamodule.dataset=TNEWS \
# huffingface的预训练模型都会支持
datamodule.plm=hfl/chinese-roberta-wwm-ext \ 
datamodule.batch_size=32 \
model=bert_tc \
model.lr=3e-5 \
seed=1234 \
trainer=default
# 默认为单gpu 0号显卡训练,可以通过以下方式修改显卡
# trainer.devices=[1]
# 单卡半精度训练
# trainer.precision=16
# 使用wandb记录日志
# logger=wandb
# 多卡训练
# trainer=ddp trainer.devices=4
```

> 模型预测
```python
from nlhappy.models import BertTextClassification
# 加载训练的checkpoint
ckpt = 'logs/path/***.ckpt'
model = BertTextClassification.load_from_ckeckpoint(ckpt)
text = '研究开始前30天内，接受过其他临床方案治疗；'
scores = model.predict(text=text, device='cpu')
# 转为onnx模型
model.to_onnx('path/tc.onnx')
model.tokenizer.save_pretrained('path/tokenizer')
```
</details>

<details>
<summary><b>实体抽取</b></summary>

nlhappy支持正常,嵌套和非连续的实体抽取任务,下面以可以解决嵌套任务的模型globalpointer为例
> 制作数据集
```python
# CBLUE实体识别数据集CMeEE
from nlhappy.datamodules import EntityExtractionDataModule
from nlhappy.models.entity_extraction import GlobalPointerForEntityExtraction
from nlhappy.utils.make_dataset import Dataset, DatasetDict
import srsly

#查看数据集格式
example = EntityExtractionDataModule.show_one_example()
# example : {"text":"这是一个长颈鹿","entities":[{"indexes":[4,5,6],"label":"动物", "text":"长颈鹿"}]}

# 根据格式制作数据集
train_data = list(srsly.read_json('assets/CMeEE/CMeEE_train.json'))
val_data = list(srsly.read_json('assets/CMeEE/CMeEE_dev.json'))
def convert_to_dataset(data):
    ds = {'text':[],'entities':[]}
    for d in data:
        ents = []
        ds['text'].append(d['text'])
        for e in d['entities']:
            if len(e['entity'])>0:
                ent = {}
                ent['text'] = e['entity']
                ent['indexes'] = [idx for idx in range(len(e['entity']))]
                ent['text'] = e['entity']
                ent['label'] = e['type']
                ents.append(ent)
        ds['entities'].append(ents)
    return Dataset.from_dict(ds) 
train_ds = convert_to_dataset(train_data)
val_ds = convert_to_dataset(val_data)
dataset_dict = DatasetDict({'train':train_ds, 'validation':val_ds})
dataset_dict.save_to_disk('./datasets/CMeEE')


```
> 训练模型

- 编写训练脚本
```bash
nlhappy \
datamodule=entity_extraction \
datamodule.dataset=CMeEE \
datamodule.plm=hfl/chinese-roberta-wwm-ext \
datamodule.batch_size=16 \
model=globalpointer \
model.lr=3e-5 \
seed=123
# 默认trainer为单卡训练
trainer=default

# 多卡
# trainer=ddp \
# trainer.devices=4 \
# trainer.precision=16 #半精度

# 如果安装了wandb则可以使用wandb
# logger=wandb 
```

> 模型推理

```python
from nlhappy.models import GlobalPointer
ckpt = 'logs/path/***.ckpt'
model = GlobalPointer.load_from_ckeckpoint(ckpt)
ents = model.predcit('文本')

# 转为onnx模型,进行后续部署
model.to_onnx('path/tc.onnx')
model.tokenizer.save_pretrained('path/tokenizer')
```
</details>

<details>
<summary><b>关系抽取</b></summary>
TODO
</details>

<details>
<summary><b>事件抽取</b></summary>
TODO
</details>

<details>
<summary><b>摘要</b></summary>
TODO
</details>

<details>
<summary><b>翻译</b></summary>
TODO
</details>


## 论文复现