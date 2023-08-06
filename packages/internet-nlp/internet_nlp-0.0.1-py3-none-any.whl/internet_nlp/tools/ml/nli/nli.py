from sentence_transformers import CrossEncoder

class NLI:

    def __init__(self):
        self.model = CrossEncoder('cross-encoder/nli-deberta-v3-large')

    def setPremiseHypothesis(self, premise, hypothesis):
        self.scores = self.model.predict([(premise, hypothesis)])

    def getLabel(self):
        label_mapping = ['contradiction', 'entailment', 'neutral']
        labels = [label_mapping[score_max] for score_max in self.scores.argmax(axis=1)]
        return labels[0]
