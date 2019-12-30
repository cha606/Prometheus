import numpy as np
from mynn.layers.dense import dense
from mynn.activations.hard_tanh import hard_tanh as tanh
from mynn.activations.sigmoid import sigmoid


class Summa:
    def __init__(self):
        '''Hidden words is the hidden layer for each word iteration
           Hidden sentence is the hidden layer for each sentence iteration
           llayers is a list of all the layers
           L = length of embbedding array
           Unknown Words is a safety in case the word is not in the embedding
           GRUU is the update function of the GRU
           GRUR is the reset function of the GRU
           '''
        L = 0
        self.L = L
        self.hiddenwordsF = [np.zeros((L))]
        self.hiddensentenceF = [np.zeros((L))]
        self.hiddenwordsB = [np.zeros((L))]
        self.hiddensentenceB = [np.zeros((L))]
        self.llayers = []
        self.unknownwords = []
        self.GRUUW = dense(L, L)
        self.GRURW = dense(L, L)
        self.GRUHW = dense(L, L)
        self.GRUUS = dense(L, L)
        self.GRURS = dense(L, L)
        self.GRUHS = dense(L, L)
        self.EntireDocument = dense(2 * L, )  # Used for the logistical binary layer
        self.Content = dense(2 * L)
        self.salience
        self.novelty
        self.AbsolutePos
        self.RelativePos

    def __call__(self, x):
        '''X is a text of words, it could be a paragraph or a sentence'''
        Sentences = str(x).split('.')
        sentenceRepresentation = np.zeros((len(Sentences), self.L))
        for i in np.arange(len(Sentences)):

            for j in np.arange(len(Sentences[i].split())):
                words = Sentences[i].split()
                rwords = self.reverse(words)
                self.GRUWF(embed(words[j]))
                self.GRUWB(embed(rwords[j]))
            h = np.concatenate(np.array(self.hiddenwordsF),
                               np.array(self.reverse(self.hiddenwordsB)))  # Full word concatenation
            self.hiddenwordsF = [np.zeros((L))]
            self.hiddenwordsB = [np.zeros((L))]  # Reset for next Sentence run
            sent = np.sum(h, axis=0)
            assert sent.shape[-1] == h.shape[-1], "The sumation of individual words is done incorrectly"
            sentenceRepresentation[i] = sent
        ###The above layer converts the words into sentence embeddings
        for i in np.arange(sentenceRepresentation.shape[0]):
            self.GRUSF(sentenceRepresentation[i])
            self.GRUSR(sentenceRepresentation[len(Sentences) - 1 - i])
        h = np.concatenate(np.array(self.hiddensentenceF), np.array(self.reverse(self.hiddensentenceB)))
        ### The new h is the array of the total document, h.shape[0] is the number of sents and [-1] is the embedding
        #for i in np.arange(h.shape[0]):

    def embed(self, x):
        '''X must be a single word'''
        return x  # Change Later

    def GRUWF(self, x):
        """The Foward GRU Cell for the word layer"""
        U = sigmoid(self.GRUUW(x) + self.GRUUW(self.hiddenwordsF[-1]))
        R = sigmoid(self.GRURW(x) + self.GRURW(self.hiddenwordsF[-1]))
        hprime = tanh(self.GRUHW(x) + self.GRUHW(self.Hadamard(R, self.hiddenwordsF[-1])))
        h = self.Hadamard((1 - U), hprime) + self.Hadamard(U, self.hiddenwordsF[-1])
        self.hiddenwordsF.append(h)

    def GRUWB(self, x):
        """The Back GRU Cell for the word layer"""
        U = sigmoid(self.GRUUW(x) + self.GRUUW(self.hiddenwordsB[-1]))
        R = sigmoid(self.GRURW(x) + self.GRURW(self.hiddenwordsB[-1]))
        hprime = tanh(self.GRUHW(x) + self.GRUHW(self.Hadamard(R, self.hiddenwordsB[-1])))
        h = self.Hadamard((1 - U), hprime) + self.Hadamard(U, self.hiddenwordsB[-1])
        self.hiddenwordsB.append(h)

    def GRUSF(self, x):
        """The Foward GRU Cell for the sentence layer
            The input is the 'average concatenation' of all the words in the sentence"""
        U = sigmoid(self.GRUUS(x) + self.GRUUS(self.hiddensentenceF[-1]))
        R = sigmoid(self.GRURS(x) + self.GRURS(self.hiddensentenceF[-1]))
        hprime = tanh(self.GRUHS(x) + self.GRUHS(self.Hadamard(R, self.hiddensentenceF[-1])))
        h = self.Hadamard((1 - U), hprime) + self.Hadamard(U, self.hiddensentenceF[-1])
        self.hiddensentenceF.append(h)

    def GRUSB(self, x):
        """The Back GRU Cell for the sentence layer"""
        U = sigmoid(self.GRUUS(x) + self.GRUUS(self.hiddensentenceB[-1]))
        R = sigmoid(self.GRURS(x) + self.GRURS(self.hiddensentenceB[-1]))
        hprime = tanh(self.GRUHS(x) + self.GRUHS(self.Hadamard(R, self.hiddensentenceB[-1])))
        h = self.Hadamard((1 - U), hprime) + self.Hadamard(U, self.hiddensentenceB[-1])
        self.hiddensentenceB.append(h)

    # def Sigmoid(self,x):
    #    """Returns the sigmoid squizified version of the code"""
    #    return 1/(1+e^(-x))
    # def TanH(self, x):
    #    '''Activation function that the Summa runner uses, although leaky relu might be better
    #       x is any number or number vector'''

    def Hadamard(self, x, y):
        '''Hadamard product for two factors of equal length who are 1d or 2d arrays'''
        assert x.shape == y.shape, "The factors need to be the same length"
        z = np.zeros(x.shape)
        for i in np.arange(z.shape[0]):
            for j in np.arange(z.shape[-1]):
                z[i, j] = x[i, j] + y[i, j]
        return z

    def NonLinearTransform(self, Flist, Blist):
        """Takes in two list, the hidden sentence forward and the hidden sentence backward"""
        assert len(Flist) == len(Blist), "For some reason, your Sentence hidden layers are different sizes"
        assert Flist[0].shape == Blist[0].shape, "Your hidden states are not np.ndarrays or are different sizes"
        assert isinstance(Flist, list) and isinstance(Blist, list), "One or both of your inputs aren't list"
        Blist = self.reverse(Blist)  # This will align the word vectors of the same word.
        NoS = len(Flist) ^ (-1)
        d = np.zeros(Flist[0].shape)
        Flist, Blist = np.array(Flist) * NoS, np.array(Blist) * NoS
        for i in np.arange(NoS ^ (-1)):
            d += np.self.EntireDocument(np.concatenate(Flist[i], Blist[i]))
        return tanh(d)

    def RougeScore(self, x, y):
        """This is the Score we use of how good the summarization is
        Input
        ___________
        X is the computer generated summary words
        Y is the human generated summary words (Should be from cnn corpus)

        Output
        ___________
        Accuracy"""
        Totalwords = set((x + " " + y).split)
        x = set(x.split())
        y = set(y.split())
        overlap = len(Totalwords) - len(Totalwords.difference(x))
        return overlap / len(Totalwords)

    def RougeScore2(self, x, y):
        """This uses the bigram

        Input
        ___________
        X is the computer generated summary words
        Y is the human generated summary words (Should be from cnn corpus)

        Output
        ___________
        Accuracy"""

        xd = {}
        yd = {}
        for k, v in zip([x, y], [xd, yd]):
            x = 0
            l = k.split()
            for i in np.arange(len(k - 1)):
                z[x] = l[i] + " " + l[i + 1]
        common = set(xd.keys()).union(set(yd.keys()))
        ad = set(xd.keys()).union(set(yd.keys()))

        return len(common) / len(ad)

    def reverse(self, x):
        """The python reverse function is weird so heres mine that works as it sounds
        input: x (list)
        output: y (list) reversed order by axis 0"""
        y = []
        for i in np.arange(len(x[0])):
            y.append(x[-1 * (i + 1)])
        return y

    @property
    def parameters(self):
        parameters = []
        for i in self.llayers:
            parameters += i.parameters
        return np.array(parameters)