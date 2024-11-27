from transformers import ViltProcessor, ViltForQuestionAnswering
import requests
from PIL import Image
class VILT:

    def __init__(self):
        self.processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    def ask(self, image, text):
        # prepare inputs
        encoding = self.processor(image, text, return_tensors="pt")

        # forward pass
        outputs = self.model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        return str(self.model.config.id2label[idx])