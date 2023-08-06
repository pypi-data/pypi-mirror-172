from functools import lru_cache
import pytorch_lightning as pl
from typing import Optional,  Tuple, List, Union
from ..utils.make_datamodule import PLMBaseDataModule
import torch
import os


class TextPairClassificationDataModule(PLMBaseDataModule):
    '''句子对数据模块,用来构建pytorch_lightning的数据模块.
    dataset_example:
        {'text_a': '肺结核','text_b': '关节炎','label': 不是一种病}
    '''
    def __init__(self,
                dataset: str,
                plm: str,
                transform: str,
                batch_size: int,
                return_pair: bool=False): 
        """参数:
        - dataset: 数据集名称,feature 必须包含 text_a, text_b, label
        - plm: 预训练模型名称
        - batch_size: 批大小
        - return_pair: 是否以文本对为输入
        """ 
        super().__init__()

        # 这一行代码为了保存传入的参数可以当做self.hparams的属性
        self.save_hyperparameters(logger=False)


    @property
    @lru_cache()
    def label2id(self):
        set_labels = sorted(set([label for label in self.dataset['train']['label']]))
        return {label: i for i, label in enumerate(set_labels)}

        
    def setup(self, stage: str):
        self.hparams['label2id'] = self.label2id
        self.hparams['id2label'] = {i: label for i, label in self.label2id.items()}
        self.dataset.set_transform(transform=self.transform)
        

    def transform(self, examples):
        batch_text_a = examples['text_a']
        batch_text_b = examples['text_b']
        batch_labels = examples['label']
        batch = {'inputs_a': [], 'inputs_b': [], 'label_ids':[]}
        batch_cross = {'inputs': [], 'label_ids':[]}
        if self.hparams.return_pair:
            for i  in range(len(batch_text_a)):
                inputs_a= self.tokenizer(batch_text_a[i], 
                                        padding='max_length', 
                                        max_length=self.hparams.max_length+2, 
                                        truncation=True)
                inputs_a = dict(zip(inputs_a.keys(), map(torch.tensor, inputs_a.values())))
                batch['inputs_a'].append(inputs_a)
                inputs_b = self.tokenizer(batch_text_b[i],
                                        padding='max_length', 
                                        max_length=self.hparams.max_length, 
                                        truncation=True)
                inputs_b = dict(zip(inputs_b.keys(), map(torch.tensor, inputs_b.values())))
                batch['inputs_b'].append(inputs_b)
                batch['label_ids'].append(self.hparams['label2id'][batch_labels[i]])
            return batch
        else:
            for i in range(len(batch_text_a)):
                inputs = self.tokenizer(batch_text_a[i],
                                        batch_text_b[i], 
                                        padding='max_length', 
                                        max_length=self.hparams.max_length*2+2, 
                                        truncation=True)
                inputs = dict(zip(inputs.keys(), map(torch.tensor, inputs.values())))
                batch_cross['inputs'].append(inputs)
                batch_cross['label_ids'].append(self.hparams['label2id'][batch_labels[i]])
            return batch_cross