import nltk  
import medicalInfoGatherer
import postsGatherer
import forum

def checkForSymptomInClause(sentence):
    
    for symptom in listOfSymptoms:
        if symptom in sentence:
            return True
        
    return False

def checkForExperience(sentence):
    #TODO: Figure out mechanism to classify a sentence as an experience or not
    return False

def checkForDiseaseInClause(sentence):
    
    for disease in listOfDiseases:
        if disease in sentence:
            return True

    return False

"""The argument extraction script begins here:

    1. First we pull in list of forum posts
    2. We then pull in list of medical diseases and symptoms
    3. For each of the posts we search for the presence of symptoms or diseases in the tokenised posts
"""

# Gather the posts from all of the forums and the list of necessary medical terms 
forums = postsGatherer.gatherForums()
listOfDiseases = medicalInfoGatherer.getListofDiseases()
listOfSymptoms = medicalInfoGatherer.getListofSymptoms()

symptomsFound = []
diseasesFound = []

# Loop through each of the forum posts and print the arguments onto the page. The arguments for and against each of the posts.
# Some sort of extremley Naive Bayesian classifier 

for forum in forums:
    posts = forum.getPosts()

    print('Starting [argumentExtractor]: Beginning to search for symptoms and diseases within the posts\n')

    for post in posts:
        sentences = nltk.sent_tokenize(post.getReview())

        for sentence in sentences:
            if(checkForSymptomInClause(sentence)):
                post.setSymptoms(sentence) 
                symptomsFound.append(sentence)
            if(checkForDiseaseInClause(sentence)):
                post.setDisease(sentence)
                diseasesFound.append(sentence)
            if(checkForExperience(sentence)):
                post.setExperience(sentence)

    print('Completed [argumentExtractor]: Finished searching for symptoms and diseases within the posts\n')

 # Now run through and print off the list of symptoms and diseases found relative to the drug
 # In this simple script we have taken the reviews on tamoxifen 

print('****Starting [argumentExtractor]: Printing out all of the symptoms found:****\n')
for symptom in symptomsFound:
    print(symptom)
    print('\n')
print('Completed [argumentExtractor]: Finished printing\n')

print('****Starting [argumentExtractor]: Printing out all of the diseases found:****\n')
for disease in diseasesFound:
    print(disease)
    print('\n')
print('Completed [argumentExtractor]: Finished printing\n')
    