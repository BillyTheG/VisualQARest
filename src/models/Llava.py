from PIL import Image

import torch
from transformers import AutoProcessor, AutoModelForPreTraining

class Llava:

    def __init__(self):
        self.model_id = "OpenFace-CQUPT/Human_LLaVA"
        self.cuda = 0
        self.model = AutoModelForPreTraining.from_pretrained("OpenFace-CQUPT/Human_LLaVA", torch_dtype=torch.float16).to(self.cuda)
        self.processor = AutoProcessor.from_pretrained(self.model_id, trust_remote_code=True)



    def ask(self, image, text):

        prompt = "USER: <image>\n" + text + "\nASSISTANT:"
        # raw_image = Image.open(requests.get(image_file, stream=True).raw)
        inputs = self.processor(images=image, text=prompt, return_tensors='pt').to(self.cuda, torch.float16)

        output = self.model.generate(**inputs, max_new_tokens=400, do_sample=False)
        predict = self.processor.decode(output[0][:], skip_special_tokens=True)

        return str(predict)