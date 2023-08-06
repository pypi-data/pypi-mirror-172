from transformers import AutoTokenizer


class StrideformerTokenizer:

    def __init__(self, max_length, stride):

        self.max_length = max_length
        self.stride = stride
        self.tokenizer = None

    def __call__(self, *args, **kwargs):

        return self.tokenizer(
            *args, 
            **kwargs, 
            max_length=self.max_length,
            stride=self.stride,
            padding=True,
            truncation=True,
            return_overflowing_tokens=True
            )
        
    @classmethod
    def from_pretrained(cls, model_name_or_path, max_length, stride):
        tokenizer = StrideformerTokenizer(max_length, stride)

        tokenizer.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

        return tokenizer

    def save_pretrained(self, path):
        self.tokenizer.save_pretrained(path)
