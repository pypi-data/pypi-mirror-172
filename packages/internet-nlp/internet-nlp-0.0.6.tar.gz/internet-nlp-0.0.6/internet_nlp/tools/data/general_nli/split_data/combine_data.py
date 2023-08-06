from datasets import load_dataset_builder, load_dataset, get_dataset_split_names, get_dataset_config_names
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(str(Path(__file__).parent.parent.parent.parent) + "/normalizer"))
import normalize

class NLIDataToCsv:

    def __init__(self, snliCsv="", multinliCsv="", anliCsv="", dataCsv="", premise=[], hypothesis=[], label=[]):
        self.snliCsv = snliCsv
        self.multinliCsv = multinliCsv
        self.anliCsv = anliCsv
        self.dataCsv = dataCsv
        self.premise = premise
        self.hypothesis = hypothesis
        self.label = label
        self.Normalizer = normalize.NormalizeTextClass()

    def normalize(self, text):
        self.Normalizer.setInputText(str(text))
        self.Normalizer.doAllCommands()
        return self.Normalizer.getNormalizedText()

    def setSnliCsv(self, snliCsv):
        self.snliCsv = snliCsv
    
    def setMultinliCsv(self, multinliCsv):
        self.multinliCsv = multinliCsv

    def setAnliCsv(self, anliCsv):
        self.anliCsv = anliCsv 

    def setDataCsv(self, dataCsv):
        self.dataCsv = dataCsv

    def snliToCsv(self):
        snli = load_dataset("snli")
        dfTest = pd.DataFrame(snli['test'])
        dfTest = dfTest.iloc[1: , :]
        dfTrain = pd.DataFrame(snli['train'])
        dfTrain = dfTrain.iloc[1: , :]
        dfVal = pd.DataFrame(snli['validation'])
        dfVal = dfVal.iloc[1:, :]
        df = pd.concat([dfTest, dfTrain, dfVal])
        premise = []
        for i in df['premise'].tolist():
            premise.append(self.normalize(str(i)))
        hypothesis = []
        for i in df['hypothesis'].tolist():
            hypothesis.append(self.normalize(str(i)))
        label = [] 
        for i in df['label'].tolist():
            label.append(int(i))
        self.premise += premise
        self.hypothesis += hypothesis
        self.label += label
        snliData = {
            'premise': premise,
            'hypothesis': hypothesis,
            'label': label
        }
        df = pd.DataFrame(snliData)
        print("snli")
        print("--------")
        print(df.head())
        df.to_csv(self.snliCsv, mode='a', index=False, header=True)

    def multinliToCsv(self):
        multinli = load_dataset("multi_nli")
        dfTrain = pd.DataFrame(multinli['train'])
        dfTrain = dfTrain.iloc[1:, :]
        dfValMat = pd.DataFrame(multinli['validation_matched'])
        dfValMat = dfValMat.iloc[1:, :]
        dfValMisMat = pd.DataFrame(multinli['validation_mismatched'])
        dfValMisMat = dfValMisMat.iloc[1:, :]
        df = pd.concat([dfTrain, dfValMat, dfValMisMat])
        #df = df.drop(columns=['promptID (int32)', 'pairID (string)', 'premise_binary_parse (string)', 'premise_parse (string)', 'hypothesis_binary_parse (string)', 'hypothesis_parse (string)', 'genre (string)'], axis=1)
        premise = []
        for i in df['premise'].tolist():
            premise.append(self.normalize(str(i)))
        hypothesis = []
        for i in df['hypothesis'].tolist():
            hypothesis.append(self.normalize(str(i)))
        label = []
        for i in df['label'].tolist():
            label.append(int(i))
        self.premise += premise
        self.hypothesis += hypothesis
        self.label += label
        multinliData = {
            'premise': premise,
            'hypothesis': hypothesis,
            'label': label
        }
        df = pd.DataFrame(multinliData)
        print("multinli")
        print("--------")
        print(df.head())
        df.to_csv(self.multinliCsv, mode='a', index=False, header=True)

    def anliToCsv(self):
        anli = load_dataset("anli")
        dfTrainR1 = pd.DataFrame(anli['train_r1'])
        dfTrainR1 = dfTrainR1.iloc[1:, :]
        dfDevR1 = pd.DataFrame(anli['dev_r1'])
        dfDevR1 = dfDevR1.iloc[1:, :]
        dfTestR1 = pd.DataFrame(anli['test_r1'])
        dfTestR1 = dfTestR1.iloc[1:, :]
        dfTrainR2 = pd.DataFrame(anli['train_r2'])
        dfTrainR2 = dfTrainR2.iloc[1:, :]
        dfDevR2 = pd.DataFrame(anli['dev_r2'])
        dfDevR2 = dfDevR2.iloc[1:, :]
        dfTestR2 = pd.DataFrame(anli['test_r2'])
        dfTestR2 = dfTestR2.iloc[1:, :]
        dfTrainR3 = pd.DataFrame(anli['train_r3'])
        dfTrainR3 = dfTrainR3.iloc[1:, :]
        dfDevR3 = pd.DataFrame(anli['dev_r3'])
        dfDevR3 = dfDevR3.iloc[1:, :]
        dfTestR3 = pd.DataFrame(anli['test_r3'])
        dfTestR3 = dfTestR3.iloc[1:, :]
        df = pd.concat([dfTestR1, dfTestR2, dfTestR3, dfTrainR1, dfTrainR2, dfTrainR3, dfDevR1, dfDevR2, dfDevR3])
        premise = []
        for i in df['premise'].tolist():
            premise.append(self.normalize(str(i)))
        hypothesis = []
        for i in df['hypothesis'].tolist():
            hypothesis.append(self.normalize(str(i)))
        label = []
        for i in df['label'].tolist():
            label.append(int(i))
        self.premise += premise
        self.hypothesis += hypothesis
        self.label += label
        anliData = {
            'premise': premise,
            'hypothesis': hypothesis,
            'label': label
        }
        df = pd.DataFrame(anliData)
        print("anli")
        print("--------")
        print(df.head())
        df.to_csv(self.anliCsv, mode='a', index=False, header=True)

    def allDataToCsv(self):
        data = {
            'premise': self.premise,
            'hypothesis': self.hypothesis,
            'label': self.label
        }
        df = pd.DataFrame(data)
        df.to_csv(self.dataCsv, mode='a', index=False, header=True)

    def doAllCommands(self):
        self.snliToCsv()
        self.multinliToCsv()
        self.anliToCsv()
        self.allDataToCsv()


