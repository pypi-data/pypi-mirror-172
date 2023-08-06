from functools import lru_cache
from typing import Tuple, List, Dict
from ..utils.make_datamodule import PLMBaseDataModule
from ..utils import utils
import torch

log = utils.get_logger(__name__)


class TextClassificationDataModule(PLMBaseDataModule):
    '''
    文本分类
    '''
    def __init__(self,
                dataset: str,
                batch_size: int ,
                plm: str = 'hfl/chinese-roberta-wwm-ext',
                transform: str = 'bert_tc',
                **kwargs):
        """单文本分类数据模块

        Args:
            dataset (str): 数据集名称
            plm (str): 预训练模型名称
            batch_size (int): 批次大小
            transform (str): 数据转换形式,默认为simple
            num_workers (int, optional): 进程数. Defaults to 0.
            pin_memory (bool, optional): . Defaults to False.
            plm_dir (str, optional): 自定义预训练模型文件夹. Defaults to './plms/'.
            dataset_dir (str, optional): 自定义数据集文件夹. Defaults to './datasets/'.
        """
        
        super().__init__()        
        self.transforms = {'bert_tc': self.bert_transform}
        assert self.hparams.transform in self.transforms.keys(), f'available models for text classification dm: {self.transforms.keys()}'
        
        
    def setup(self, stage: str = 'fit') -> None:
        self.hparams.max_length = self.get_max_length()
        self.hparams.label2id = self.label2id
        self.hparams.id2label = {i:l for l, i in self.label2id.items()}
        self.dataset.set_transform(transform=self.transforms.get(self.hparams.transform))

    
    def bert_transform(self, examples) -> Dict:
        batch_text = examples['text']
        batch_label_ids = []
        max_length = self.hparams.max_length
        batch_inputs = self.tokenizer(batch_text,
                                      padding='max_length',
                                      max_length=max_length,
                                      truncation=True,
                                      return_tensors='pt')
        for i, text in enumerate(batch_text):
            label_id = self.hparams['label2id'][examples['label'][i]]
            batch_label_ids.append(label_id)
        batch_inputs['label_ids'] = torch.LongTensor(batch_label_ids)        
        return batch_inputs


    @property
    @lru_cache()
    def label2id(self):
        labels = sorted(set(self.train_df.label.values))
        label2id = {l : i for i,l in enumerate(labels)}
        return label2id


    @property
    def id2label(self):
        return {i:l for l,i in enumerate(self.label2id)}

        
    @classmethod
    def get_one_example(cls):
        return {'label': '新闻', 'text': '怎么给这个图片添加超级链接呢？'}
    
    
    @classmethod
    def get_available_transforms(cls):
        return ['bert']
        