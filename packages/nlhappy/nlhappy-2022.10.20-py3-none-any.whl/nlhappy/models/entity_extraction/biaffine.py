from ...utils.make_model import PLMBaseModel, align_token_span
from ...layers.classifier import BiaffineSpanClassifier
from ...layers.dropout import MultiDropout
from ...layers.loss import MultiLabelCategoricalCrossEntropy
from ...metrics.span import SpanF1
import torch


class BiaffineForEntityExtraction(PLMBaseModel):
    def __init__(self,
                 lr: float = 3e-5,
                 hidden_size: int = 128,
                 add_rope: bool = True,
                 threshold: float = 0.0,
                 scheduler: str = 'linear_warmup_step',
                 weight_decay: float = 0.01,
                 **kwargs) -> None:
        super().__init__()
        
        self.plm = self.get_plm_architecture()
        self.classifier = BiaffineSpanClassifier(input_size=self.plm.config.hidden_size,
                                                 hidden_size=hidden_size,
                                                 output_size=len(self.hparams.label2id),
                                                 add_rope=add_rope)
        self.dropout = MultiDropout()
        
        self.criterion = MultiLabelCategoricalCrossEntropy()

        self.train_metric = SpanF1()
        self.val_metric = SpanF1()
        self.test_metric = SpanF1()


    def forward(self, input_ids, token_type_ids, attention_mask):
        x = self.plm(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask).last_hidden_state
        x = self.dropout(x)
        x = self.classifier(x, mask=attention_mask)
        return x
    
    
    def step(self, batch):
        input_ids = batch['input_ids']
        token_type_ids = batch['token_type_ids']
        attention_mask = batch['attention_mask']
        span_ids = batch['label_ids']
        logits = self(input_ids, token_type_ids, attention_mask)
        pred = logits.ge(self.hparams.threshold).float()
        batch_size, ent_type_size = logits.shape[:2]
        y_true = span_ids.reshape(batch_size*ent_type_size, -1)
        y_pred = logits.reshape(batch_size*ent_type_size, -1)
        loss = self.criterion(y_pred, y_true)
        return loss, pred, span_ids

        
    def training_step(self, batch, batch_idx):
        loss, pred, true = self.step(batch)
        self.train_metric(pred, true)
        self.log('train/f1', self.train_metric, on_step=True, on_epoch=True, prog_bar=True)
        return {'loss':loss}
    
    
    def validation_step(self, batch, batch_idx):
        loss, pred, true = self.step(batch)
        self.val_metric(pred, true)
        self.log('val/f1', self.val_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'loss':loss}
    
    
    def test_step(self, batch, batch_idx):
        loss, pred, true = self.shared_step(batch)
        self.test_metric(pred, true)
        self.log('test/f1', self.test_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'loss': loss}
    
    
    def configure_optimizers(self):
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        grouped_parameters = [
            {'params': [p for n, p in self.plm.named_parameters() if not any(nd in n for nd in no_decay)],
             'lr': self.hparams.lr, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.plm.named_parameters() if any(nd in n for nd in no_decay)],
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