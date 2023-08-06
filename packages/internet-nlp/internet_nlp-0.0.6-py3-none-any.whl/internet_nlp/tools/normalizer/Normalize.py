import string
import contractions
import tokenizers
from tokenizers.normalizers import Lowercase, NFKD, StripAccents
import re
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import Constants

class NormalizeTextClass:

    def __init__(self, inputText = "", outputText=""):
        self.inputText = inputText
        self.outputText = outputText
        self.normalierSeq = tokenizers.normalizers.Sequence([Lowercase(), NFKD(), StripAccents()])
        for i in Constants.contractionsDict:
            contractions.add(i, Constants.contractionsDict[i])

    def setInputText(self, inputTextIn):
        self.inputText = str(inputTextIn)
        self.outputText = str(inputTextIn)

    def expandContradictions(self):
        self.outputText = contractions.fix(self.inputText)

    def normalize(self):
        self.outputText = self.normalierSeq.normalize_str(self.outputText)

    def removePunctuation(self):
        # Remove punctuation from sentence
        tmp = self.outputText.translate(str.maketrans('', '', string.punctuation))
        tmp = re.sub(r'[^\w\s]', '', tmp)
        tmp = tmp.replace('', '')
        tmp = tmp.lower()
        self.outputText = tmp

    def doAllCommands(self):
        self.expandContradictions()
        self.removePunctuation()
        self.normalize()
        
    def getNormalizedText(self):
        return self.outputText


"""
normalier = NormalizeTextClass()
testingInput = "It would be unfair to demand that people cease pirating files when those same people aren't paid for their participation in very lucrative network schemes. Ordinary people are relentlessly spied on, and not compensated for information taken from them. While I'd like to see everyone eventually pay for music and the like, I'd not ask for it until there's reciprocity."
normalier.setInputText(testingInput)
print(normalier.getNormalizedText())
"""
