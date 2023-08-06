from transformers import pipeline

class OpenBookQA:

    def __init__(self):
        self.MODELNAME = "mrm8488/longformer-base-4096-finetuned-squadv2"
        self.model = pipeline("question-answering", model=self.MODELNAME, tokenizer=self.MODELNAME)

    def setQuestionContext(self, question, context):
        self.question = question
        self.context = context

    def getResult(self):
        res = self.model(question = self.question, context = self.context)
        return str(res['answer'])
