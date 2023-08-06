from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

class SentenceToQuestion:

    def __init__(self):
        self.MODELNAME = "ramsrigouthamg/t5_squad_v1"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODELNAME)
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODELNAME)
        # self.answertokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")
        # self.answermodel = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")

    def getQuestion(self, forumAns, forumQues):
        mdl = self.model
        tknizer = self.tokenizer
        sentence = forumAns
        answer = forumQues
        text = "context: {} answer: {}".format(sentence,answer)
        # print (text)
        max_len = 256
        encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")
        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]
        outs = mdl.generate(input_ids=input_ids,
                                        attention_mask=attention_mask,
                                        early_stopping=True,
                                        num_beams=5,
                                        num_return_sequences=1,
                                        no_repeat_ngram_size=2,
                                        max_length=300)
        dec = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
        Question = dec[0].replace("question:","")
        Question= Question.strip()
        return Question

    def getQuestionWithoutQuestion(self, response):
        mdl = self.model
        tknizer = self.tokenizer
        sentence = response
        text = "context: {}".format(sentence)
        # print (text)
        max_len = 256
        encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")
        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]
        outs = mdl.generate(input_ids=input_ids,
                                        attention_mask=attention_mask,
                                        early_stopping=True,
                                        num_beams=5,
                                        num_return_sequences=1,
                                        no_repeat_ngram_size=2,
                                        max_length=300)
        dec = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
        Question = dec[0].replace("question:","")
        Question= Question.strip()
        return Question
        
