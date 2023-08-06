from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class CBQA:

    def __init__(self):
        self.MODELNAME = "google/t5-xxl-ssm-tqa"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODELNAME)
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODELNAME)

    def setPrompt(self, prompt):
        self.prompt = prompt

    def getResult(self):
        input_ids = self.tokenizer(self.prompt, return_tensors="pt").input_ids
        gen_output = self.model.generate(input_ids)[0]
        return str(self.tokenizer.decode(gen_output, skip_special_tokens=True))
