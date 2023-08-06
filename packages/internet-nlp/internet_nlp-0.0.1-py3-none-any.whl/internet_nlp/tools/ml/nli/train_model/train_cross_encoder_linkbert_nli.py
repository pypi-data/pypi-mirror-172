# sentence embedding via sbert's library along side linkBERT-large to enable a new unique model which will perform generally more accurately than either bert-large nli via word embedding

from sentence_transformers import SentenceTransformer, models

# imports
import math
from sentence_transformers import InputExample, losses
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CESoftmaxAccuracyEvaluator
from torch.utils.data import DataLoader
from sentence_transformers import evaluation
import pandas as pd
from pathlib import Path

class ML:

    def __init__(self, EVALSTEPS, NUMEPOCHS, WARMUPSTEPS, MODELPATH, csvPath=""):
        #self.MODELNAME = "facebook/bart-large-mnli"
        #self.EVALSTEPS = 50
        #self.NUMEPOCHS = 20
        #self.WARMUPSTEPS = 100
        #self.MODELPATH = "./download/"
        self.MODELNAME = "michiyasunaga/LinkBERT-large"
        self.EVALSTEPS = EVALSTEPS
        self.NUMEPOCHS = NUMEPOCHS
        self.WARMUPSTEPS = WARMUPSTEPS
        self.MODELPATH = MODELPATH
        self.csvPath = csvPath

    def setCsvPath(self, csvPath):
        self.csvPath = csvPath
        print("DONE WITH SETTING CSV PATH")

    def readCsv(self):
        self.df = pd.read_csv(self.csvPath)
        print("DONE WITH READING CSV PATH")

    def dataModified(self):
        self.int2label = {0: "contradiction", 1 : "neutral", 2: "entailment"}
        self.trainingData = []
        self.testingData = []
        self.premise = []
        self.hypothesis = []
        self.label = []
        i = 0
        for idx, row in self.df.iterrows():
            i += 1
            if (i % 100 == 0):
                self.testingData.append(InputExample(texts=[row['premise'], row['hypothesis']], label=row['label']))
            tmp = row["label"]
            if (not(tmp == 0 or tmp ==1 or tmp == 2)):
                continue
            self.trainingData.append(InputExample(texts=[row['premise'], row['hypothesis']], 
                                                  label=row['label']))
            self.premise.append(row['premise'])
            self.hypothesis.append(row['hypothesis'])
            self.label.append(row['label'])
        print("DONE WITH DATA MODIFICATION")

    def trainModel(self):
        self.model = CrossEncoder(self.MODELNAME, 
                                  num_labels=len(self.int2label))
        self.trainDataloader = DataLoader(self.trainingData, 
                                          shuffle=True, 
                                          batch_size=16)
        # crossentropy loss
        # self.trainLoss = losses.SoftmaxLoss(model=self.model, 
        #                                     sentence_embedding_dimension=self.model.get_sentence_embedding_dimension(), 
        #                                     num_labels=3)
        # self.evaluator = evaluation.EmbeddingSimilarityEvaluator(self.premise, 
        #                                                          self.hypothesis, 
        #                                                          self.label)
        self.evaluator = CESoftmaxAccuracyEvaluator.from_input_examples(self.testingData, name='alotnli-dev')
        # self.model.fit(train_objectives=[(self.trainDataloader, self.trainLoss)],
        #           evaluator=self.evaluator,
        #           evaluation_steps=self.EVALSTEPS,
        #           epochs=self.NUMEPOCHS,
        #           warmup_steps=self.WARMUPSTEPS,
        #           output_path=self.MODELPATH)
        print("GETTING READY TO TRAIN")
        warmup_steps = math.ceil(len(self.trainDataloader) * self.NUMEPOCHS * 0.1) #10% of train data for warm-up
        self.model.fit(train_dataloader=self.trainDataloader,
                  evaluator=self.evaluator,
                  evaluation_steps=self.EVALSTEPS,
                  epochs=self.NUMEPOCHS,
                  warmup_steps=warmup_steps,
                  output_path=self.MODELPATH)
        print("DONE TRAINING")

NLI = ML(EVALSTEPS=50, NUMEPOCHS=20, WARMUPSTEPS=100, MODELPATH="./download/")
def main():
    NLI.setCsvPath("https://files.thamognya.com/projects/internet-nlp/data.csv")
    NLI.readCsv()
    NLI.dataModified()
    NLI.trainModel()

main()
