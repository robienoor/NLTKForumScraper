from xml.etree import ElementTree
from xml.dom import minidom
from xml.sax.saxutils import escape
from DataLayer import forum
from DataLayer import post

def prettify(elem):
    #Return a pretty-printed XML string for the Element
    roughString = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(roughString)
    return reparsed

def constructSinglePostXML(top, forumPost):

    post = ElementTree.SubElement(top, 'post')

    website = ElementTree.SubElement(post, 'website')
    website.text = escape(forumPost.getUrl())

    originalMessage = ElementTree.SubElement(post, 'originalMessage')
    originalMessage.text = escape(forumPost.getReview())
    
    diseases = ElementTree.SubElement(post, 'diseases')
    for forumPostDisease in forumPost.getDisease():
        disease = ElementTree.SubElement(diseases, 'disease')
        disease.text = forumPostDisease
    
    symptoms = ElementTree.SubElement(post, 'symptoms')
    for forumPostSymptom in forumPost.getSymptoms():
        symptom = ElementTree.SubElement(symptoms, 'symptom')
        symptom.text = forumPostSymptom

    drugs = ElementTree.SubElement(post, 'drugsMentioned')
    for forumPostDrug in forumPost.getDrugs():
        drug = ElementTree.SubElement(drugs, 'drug')
        drug.text = forumPostDrug
    
    symptomDrugRel = ElementTree.SubElement(post, 'medicationPerSymptom')
    for forumPostSympDrugRel in forumPost.getSymptomDrugRelation():
        symptom = ElementTree.SubElement(symptomDrugRel, 'symptom')
        symptom.text = forumPostSympDrugRel[0]

        drug = ElementTree.SubElement(symptom, 'drug')
        drug.text = forumPostSympDrugRel[1]

    nounPhrases = ElementTree.SubElement(post, 'nounPhrasesFound')
    for nounPhraseFound in forumPost.getNounPhrases():
        nounPhrase = ElementTree.SubElement(nounPhrases, 'nounPhrase')
        nounPhrase.text = nounPhraseFound

    rating = ElementTree.SubElement(post, 'rating')
    rating.text = forumPost.getRating()

    positiveWordScore = ElementTree.SubElement(post, 'positiveWordScore')
    positiveWordScore.text = forumPost.getPositiveWordScore()

    sentimentAnalysis = ElementTree.SubElement(post, 'sentimentAnalysis')
    
    emotion = ElementTree.SubElement(sentimentAnalysis, 'emotion')
    emotion.text = forumPost.getEmotion()

    return post

def constructXML(forums):
    
    fileHandler = open("argumentsList.xml", "w")
    top = ElementTree.Element('allPosts')

    for forum in forums:
        forumPosts = forum.getPosts()

        
        for forumPost in forumPosts:
            singlePost = constructSinglePostXML(top, forumPost)

    prettifiedTop = prettify(top)

    prettifiedTop.writexml(fileHandler);

    fileHandler.close()

