from nltk.tokenize import word_tokenize
import medicalInfoGatherer
import postsGatherer
import forum
import logging
import displayArguments
import messageCleaner

class argumentExtractor(object):


    def __init__(self, listOfSymptoms, listOfDiseases, listOfInverters, listOfPosWords, listOfNegWords):
        self.listOfSymptoms = listOfSymptoms
        self.listOfDiseases = listOfDiseases
        self.listIfInverters = listOfInverters
        self.listOfPosWords = listOfPosWords
        self.listOfNegWords = listOfNegWords

    def checkForSymptomInClause(self, sentence):
    
        for symptom in self.listOfSymptoms:
            if symptom.lower() in sentence.lower():
                return (True, symptom)
        
        return (False, '')

    def checkForDiseaseInClause(self, sentence):

        for disease in self.listOfDiseases:
            if disease.lower() in sentence.lower():
                return (True, disease)

        return (False,'')

    def checkForEmotion(self, post):
        ratingCategory = ''
        volumeofDisSymptms = ''
        emotion = ''

        # Get the rating level
        rating = float(post.getRating())
        if rating <= 3:
            ratingCategory = 'low'
        elif rating >= 7:
            ratingCategory = 'high'
        else:
            ratingCategory = 'med'

        # Gauge the volume of symptoms and symptoms
        noOfSymptoms = len(post.getSymptoms())
        noOfDiseases = len(post.getDisease())
  
        if (noOfDiseases + noOfSymptoms) < 1:
            volumeofDisSymptms = 'low'
        elif (noOfDiseases + noOfSymptoms) == 1:
            volumeofDisSymptms = 'med'
        else:
            volumeofDisSymptms = 'high'

        # Primitive rules for getting the emotion
        if (volumeofDisSymptms is 'high' and ratingCategory is 'low'):
            emotion = 'unoptimisitic'
        elif (volumeofDisSymptms is 'high' and ratingCategory is 'high'):
            emotion = 'optimistic'
        elif (volumeofDisSymptms is 'low' and ratingCategory is 'high'):
            emotion = 'positive'
        else:
            emotion = 'neutral'

        return emotion

    def calculateWordScore(self, sentence):
        # import neg and pos words
        # count the number of pos words in the sentence
        # count the number of neg words in the sentence
        # do a sum of the two: score = posCount - negCount
        sentenceTokenised = word_tokenize(sentence)

        #posWords = 'Data/positive-words.txt'
        #negWords = 'Data/negative-words.txt'

        #with open(posWords) as f:
        #    posData = f.readlines()
  
        #posList = []
        #for member in posData: 
        #    member = messageCleaner.removeSpecialCharacter(member)
        #    posList.append(member)

        #with open(negWords) as f:
        #    negData = f.readlines()
  
        #negList = []
        #for member in negData: 
        #    member = messageCleaner.removeSpecialCharacter(member)
        #    negList.append(member)
    
        negScore = 0
        posScore = 0

        for i, word in enumerate(sentenceTokenised):
            score = self.__searchForMatchingToken(word, i, sentenceTokenised, self.listOfPosWords)

            if score < 0:
                negScore = negScore + score
            else:
                posScore = posScore + score

        totalScore = posScore + negScore

        return totalScore

    def __searchForMatchingToken(self, word, index, sentence, list):

        """This method will search for inverters like 'not', 'no' etc. 
            It works as follows:
                1. Search to see if the word exists in the list you are searching in
                    1. If it is the first word in the sentence (known from its index) assume it as a positive existance and return 1
                    2. If it is not the first word in the sentence, it may be that there is an inverter before it
                        1. If there is an inverter assume that it is a negative existance and return -1
                        2. Id there is not an inveter assum that it is a positive existance and return 1
                    3. If the word does not exist at all return 0
        """

        if word in list:
            if index > 0:
                if sentence[index - 1] in self.listIfInverters:
                    return -1
                else:
                    return 1
            else:
                return 1
        else:
            return 0

