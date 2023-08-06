from pathlib import Path
import sys
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/normalizer"))
import Normalize
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/ml/sentence_to_question"))
import SentenceToQuestion
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/ml/closed_book_qa"))
import ClosedBookQA
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/data/search"))
import Search
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/ml/nli"))
import Nli
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/ml/open_book_qa"))
import OpenBookQA
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/tools/ml/summarize"))
import Summarize

class NoContextQA:

    def __init__(self):
        self.STQ = SentenceToQuestion.SentenceToQuestion()
        self.CBQA = ClosedBookQA.ClosedBookQA()
        self.SLD = Search.SearchLinkData()
        self.NLI = Nli.Nli()
        self.NTC = Normalize.NormalizeTextClass()
        self.OBQA = OpenBookQA.OpenBookQA()
        self.SUM = Summarize.Summarize()

    # atleast one of these
    def setQuestion(self, question):
        self.question = question

    def setResponse(self, response):
        self.response = response
    #

    def checkIfAtleastOne(self):
        if (not(self.question == "" and self.response == "")):
            return True
        else:
            return False

    def makeQuestion(self):
        if (self.question == ""):
            self.question = self.STQ.getQuestionWithoutQuestion(self.response)
        else:
            # rephrase question
            self.question = self.STQ.getQuestion(self.response, self.question)

    def makeResponse(self):
        # make sample response
        if (self.response == ""):
            self.CBQA.setPrompt(self.question)
            self.response = self.CBQA.getResults()
    
    def searchAnswer(self):
        self.SLD.setQuestion(self.question)
        self.SLD.getWebsiteData()
        self.answers = self.SLD.getSentences()

    def checkCorrectOrWrongAnswer(self):
        self.labels = {"contradiction": 0, "entailment": 0}
        self.contexts = []
        for i in self.answers:
            i = str(i)
            self.NLI.setPremiseHypothesis(self.response, i)
            label = self.NLI.getLabel()
            if (label == "contradiction" or label == "entailment"):
                self.labels[label] += 1
                self.contexts.append(i)
        if (self.labels["contradiction"] > self.labels["entailment"]):
            self.boolAnswer = False
        elif (self.labels["contradiction"] > self.labels["entailment"]):
            self.boolAnswer = True
        else:
            self.boolAnswer = "error"

    def answerQuestionWithContext(self):
        if (self.boolAnswer != "error"):
            self.context = ""
            for i in self.context:
                self.context += str(i)
            self.NTC.setInputText(self.context)
            self.NTC.doAllCommands()
            self.context = self.NTC.getNormalizedText()
            self.OBQA.setQuestion(self.question, self.context)
            self.answer = str(self.QBQA.getResult())
        else:
            print("ERROR")
            exit()

    def summarize(self):
        if (self.answer.count(" ") + 1 >= 125):
            self.SUM.setText(self.answer)
            self.answer = self.SUM.getSummarizedText()

    def doAllCommands(self):
        if (not(self.checkIfAtleastOne())):
            print("Give atleast one")
            exit()
        self.makeQuestion()
        self.makeResponse()
        self.searchAnswer()
        self.checkCorrectOrWrongAnswer()
        while (self.boolAnswer == "error"):
            self.searchAnswer()
            self.checkCorrectOrWrongAnswer()
        self.answerQuestionWithContext()
        self.summarize()

    def getAnswer(self):
        return self.answer
