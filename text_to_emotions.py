import nltk
import text2emotion as te

def get_emotion(text):
    happy = 0
    angry = 0
    surprise = 0
    sad = 0
    fear = 0
    
    for sentence in nltk.sent_tokenize(text):
        emotions = te.get_emotion(sentence)

        happy += emotions['Happy']
        angry += emotions['Angry']
        surprise += emotions['Surprise']
        sad += emotions['Sad']
        fear += emotions['Fear']
    
    emotions = [happy, angry, surprise, sad, fear]
    
    highest_score = 0
    for emotion in emotions:
        if emotion > highest_score:
            highest_score = emotion
    
    if highest_score == happy:
        return 'happy'
    elif highest_score == angry:
        return 'angry'
    elif highest_score == sad:
        return 'sad'
    elif highest_score == surprise:
        return 'surprise'
    else:
        return 'fear'