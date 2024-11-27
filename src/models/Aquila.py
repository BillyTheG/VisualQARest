from llava.model.builder import load_pretrained_model
from llava.mm_utils import process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from llava.conversation import conv_templates
from PIL import Image
import requests
import copy
import torch
import warnings

warnings.filterwarnings("ignore")

class Aquila:

    def __init__(self):

        self.pretrained = "BAAI/Aquila-VL-2B-llava-qwen"

        self.model_name = "llava_qwen"
        self.device = "cuda"
        self.device_map = "auto"
        self.tokenizer, self.model, self.image_processor, self.max_length = load_pretrained_model(self.pretrained, None, self.model_name, device_map=self.device_map)  # Add any other thing you want to pass in llava_model_args
        self.model.eval()


    def ask(self, image, text):

        image_tensor = process_images([image], self.image_processor, self.model.config)
        image_tensor = [_image.to(dtype=torch.float16, device=self.device) for _image in image_tensor]

        conv_template = "qwen_1_5"  # Make sure you use correct chat template for different models
        question = DEFAULT_IMAGE_TOKEN + text
        conv = copy.deepcopy(conv_templates[conv_template])
        conv.append_message(conv.roles[0], question)
        conv.append_message(conv.roles[1], None)
        prompt_question = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt_question, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).to(self.device)
        image_sizes = [image.size]

        cont = self.model.generate(
            input_ids,
            images=image_tensor,
            image_sizes=image_sizes,
            do_sample=False,
            temperature=0,
            max_new_tokens=4096,
        )

        text_outputs = self.tokenizer.batch_decode(cont, skip_special_tokens=True)

        return str(text_outputs)