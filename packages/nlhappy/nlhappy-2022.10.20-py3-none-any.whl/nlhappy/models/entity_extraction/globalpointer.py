import torch.nn as nn
import torch
from ...metrics.span import SpanF1
from ...utils.make_model import PLMBaseModel, align_token_span
from ...layers import MultiLabelCategoricalCrossEntropy, EfficientGlobalPointer, MultiDropout, GlobalPointer
from ...tricks.adversarial_training import adversical_tricks
from typing import Optional


class GlobalPointerForEntityExtraction(PLMBaseModel):
    """基于globalpointer的实体识别模型,可以统一处理嵌套和非嵌套模型
    
    参考:
        - https://kexue.fm/archives/8373
        
    参数:
        - lr (float): 学习率
        - hidden_size (int): globalpointer中间层维度
        - use_efficient (bool): 是否用Efficient globalpointer
        - scheduler (str): 学习率变化器,[harmonic_epoch, linear_warmup_step, cosine_warmup_step]之一
        - span_get_type (str): globalpointer得到span特征的方式,[dot, element-product, element-add]之一
        - weight_decay (float): 权重衰减
        - adv Optinal[str]: 对抗训练方式, fgm, pgd之一
        - threshold (float): 阈值
        - add_rope (bool): 是否添加RoPE位置矩阵
        - **kwargs datamodule的hparams
    """
    def __init__(self,
                 lr: float = 3e-5,
                 hidden_size: int = 128,
                 use_efficient: bool = False,
                 scheduler: str = 'harmonic_epoch',
                 span_get_type: str = 'dot',
                 weight_decay: float = 0.01,
                 adv: Optional[str] = None,
                 threshold: float = 0.0,
                 add_rope: bool = True,
                 **kwargs) : 
        super().__init__()
        ## 手动optimizer 可参考https://pytorch-lightning.readthedocs.io/en/stable/common/optimizers.html#manual-optimization
        self.automatic_optimization = False    


        self.bert = self.get_plm_architecture()
        if use_efficient:
            self.classifier = EfficientGlobalPointer(input_size=self.bert.config.hidden_size, 
                                                 hidden_size=hidden_size,
                                                 output_size=len(self.hparams.label2id),
                                                 RoPE=self.hparams.add_rope)
        else:
            self.classifier = GlobalPointer(input_size=self.bert.config.hidden_size,
                                            hidden_size=hidden_size,
                                            output_size=len(self.hparams.label2id),
                                            add_rope=self.hparams.add_rope,
                                            span_get_type=self.hparams.span_get_type)

        self.dropout = MultiDropout()
        self.criterion = MultiLabelCategoricalCrossEntropy()

        self.train_metric = SpanF1()
        self.val_metric = SpanF1()
        self.test_metric = SpanF1()


    def forward(self, input_ids, token_type_ids, attention_mask=None):
        x = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask).last_hidden_state
        x = self.dropout(x)
        logits = self.classifier(x, mask=attention_mask)
        return logits


    def on_train_start(self) -> None:
        if self.hparams.adv :
            self.adv = adversical_tricks.get(self.hparams.adv)(self.bert)


    def shared_step(self, batch):
        span_ids = batch['label_ids']
        logits = self(input_ids=batch['input_ids'], token_type_ids=batch['token_type_ids'], attention_mask=batch['attention_mask'])
        pred = logits.ge(self.hparams.threshold).float()
        batch_size, ent_type_size = logits.shape[:2]
        y_true = span_ids.reshape(batch_size*ent_type_size, -1)
        y_pred = logits.reshape(batch_size*ent_type_size, -1)
        loss = self.criterion(y_pred, y_true)
        return loss, pred, span_ids


    def training_step(self, batch, batch_idx):
        optimizer = self.optimizers()
        optimizer.zero_grad()
        scheduler = self.lr_schedulers()
        loss, pred, true = self.shared_step(batch)
        self.manual_backward(loss)
        if self.hparams.adv == 'fgm':
            self.adv.attack()
            loss_adv,  _,  _ = self.shared_step(batch)
            self.manual_backward(loss_adv)
            self.adv.restore()
            self.log_dict({'train_loss': loss, 'adv_loss': loss_adv}, prog_bar=True)
        elif self.hparams.adv == "pgd":
            self.adv.backup_grad()
            K=3
            for t in range(K):
                self.adv.attack(is_first_attack=(t==0)) # 在embedding上添加对抗扰动, first attack时备份param.data
                if t != K-1:
                    self.zero_grad()
                else:
                    self.adv.restore_grad()
                loss_adv, _, _ = self.shared_step(batch)
                self.manual_backward(loss_adv) # 反向传播，并在正常的grad基础上，累加对抗训练的梯度
            self.adv.restore()
            self.log_dict({'train_loss': loss, 'adv_loss': loss_adv}, prog_bar=True)
        optimizer.step()
        if self.hparams.scheduler in ['harmonic_epoch']:
            if self.trainer.is_last_batch:
                scheduler.step()
        else: scheduler.step()
        self.train_metric(pred, true)
        self.log('train/f1', self.train_metric, on_step=True, on_epoch=True, prog_bar=True)
        self.log_dict({'train_loss': loss}, prog_bar=True)
        return {'loss': loss}


    def validation_step(self, batch, batch_idx):
        loss, pred, true = self.shared_step(batch)
        self.val_metric(pred, true)
        self.log('val/f1', self.val_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'loss': loss}


    def test_step(self, batch, batch_idx):
        loss, pred, true = self.shared_step(batch)
        self.test_metric(pred, true)
        self.log('test/f1', self.test_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'loss': loss}


    def configure_optimizers(self):
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        grouped_parameters = [
            {'params': [p for n, p in self.bert.named_parameters() if not any(nd in n for nd in no_decay)],
             'lr': self.hparams.lr, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.bert.named_parameters() if any(nd in n for nd in no_decay)],
             'lr': self.hparams.lr, 'weight_decay': 0.0},
            {'params': [p for n, p in self.classifier.named_parameters() if not any(nd in n for nd in no_decay)],
             'lr': self.hparams.lr * 5, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.classifier.named_parameters() if any(nd in n for nd in no_decay)],
             'lr': self.hparams.lr * 5, 'weight_decay': 0.0}
        ]
        optimizer = torch.optim.AdamW(grouped_parameters)
        scheduler_config = self.get_scheduler_config(optimizer, self.hparams.scheduler)
        return [optimizer], [scheduler_config]


    def predict(self, text: str, device: str='cpu', threshold = None):
        if threshold is None:
            threshold = self.hparams.threshold
        inputs = self.tokenizer(text,
                                add_special_tokens=True,
                                max_length=self.hparams.max_length,
                                truncation=True,
                                return_offsets_mapping=True,
                                return_tensors='pt')
        mapping = inputs.pop('offset_mapping')
        mapping = mapping[0].tolist()
        inputs.to(device)
        logits = self(**inputs)
        spans_ls = torch.nonzero(logits>threshold).tolist()
        spans = []
        for span in spans_ls :
            start = span[2]
            end = span[3]
            char_span = align_token_span((start, end+1), mapping)
            start = char_span[0]
            end = char_span[1]
            span_text = text[start:end]
            spans.append([start, end, self.hparams.id2label[span[1]], span_text])
        return spans