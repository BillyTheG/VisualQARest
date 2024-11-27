import torch
from modelscope import AutoConfig, AutoModel, AutoTokenizer

from PIL import Image
from decord import VideoReader, cpu



class Owl:

    def __init__(self):
        self.model_path = 'iic/mPLUG-Owl3-7B-240728'
        self.config = AutoConfig.from_pretrained(self.model_path, trust_remote_code=True)

        self.model = AutoModel.from_pretrained(self.model_path, attn_implementation='flash_attention_2',
                                          torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model.eval().cuda()
        self.device = "cuda"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.processor = self.model.init_processor(self.tokenizer)

    def ask(self, image, text):

        messages = [
            {"role": "user", "content": """<|image|>
                """+text},
            {"role": "assistant", "content": ""}
        ]

        inputs = self.processor(messages, images=[image], videos=None)

        inputs.to('cuda')
        inputs.update({
            'tokenizer': self.tokenizer,
            'max_new_tokens': 100,
            'decode_text': True,
        })

        return str(self.model.generate(**inputs))


