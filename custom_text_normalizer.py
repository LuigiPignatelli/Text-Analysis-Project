# HTML PARSER
import re
from bs4 import BeautifulSoup
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    [s.extract() for s in soup(['iframe', 'script'])]
    # get_text() method extracts all the text within a page
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text

# REMOVE ACCENTED CHARACTERS
import unicodedata
def remove_accented_chars(text):
    # we will be using three methods --> .normalize(), .encode() and .decode()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

# CONTRACTIONS
import contractions
dictionary = {"bc":"because",
              "idk": "i don't know",
              "awsm": "awesome",
              "af": "as fuck"}

# REMOVE SPECIAL CHARACTERS
import re
def remove_special_character(text, remove_digits=False):
    """this function removes special characters
    and digits based on remove_digits parameter"""
    
    pattern = r'[^a-zA-z0-9.!?\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern,'',text)
    return text


# SPELLING CHECKER
import nltk
from textblob import Word
from nltk.corpus import wordnet
def spelling_checker(text):
    """This function exploits the Word function
    from textblob and checks the spelling of each word"""
    
    text = text.lower()
    tokens = [token for token in nltk.word_tokenize(text)]
    tokens = [token if not wordnet.synsets(token) 
              else Word(token).correct() for token in tokens]
    text = " ".join(tokens)
    return text


# LEMMATIZATION
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
def lemmatize(text):
    """this funcion takes a piece of text
    and lemmatizes it based on pos"""
    
    tokens = nltk.word_tokenize(text)
    
    lemmas = []
    for token in nltk.pos_tag(tokens):
        # remember that token is a tuple in this case!
        if token[1] == 'VB':
            lemmas.append(wnl.lemmatize(token[0],'v'))
        elif token[1] == 'VBD' or token[1] == 'VBG' or token[1] == 'VBN':
            lemmas.append(wnl.lemmatize(token[0],'v'))
        elif token[1] == 'NN':
            lemmas.append(wnl.lemmatize(token[0],'n'))
        elif token[1] == 'JJ' or token[1] == 'JJS' or token[1] == 'JJR':
            lemmas.append(wnl.lemmatize(token[0],'a'))
        else:
            lemmas.append(token[0])

    text = ' '.join(lemmas)
    return text


# REMOVE STOPWORDS
from nltk.tokenize.toktok import ToktokTokenizer
tokenizer = ToktokTokenizer()
stop_words = nltk.corpus.stopwords.words('english')

def remove_stopwords(text, is_text_lowercase=False):
    """This function tokenizes and removes
    stop words. It takes two argument, a text
    and a boolean for lowercase text """
    
    # BASIC TOKENIZATION
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    # this removes numbers and punctuation
    #tokens = [token for token in tokens if token.isalpha()]
    
    # FILTERING + REMOVING STOPWORDS
    # if this is True our all our text, or most of it, is already lowercase
    if is_text_lowercase:
        tokens = [token for token in tokens if token not in stop_words]
    # if this is False our text is not lowercase
    else:
        tokens = [token for token in tokens if token.lower() not in stop_words]
    
    text = " ".join(tokens)
    return text

not_stopwords = ['me','my','myself','i','not','no']
for word in not_stopwords:
    if word in stop_words:
        stop_words.remove(word)
        

        
        
def normalize_corpus(corpus, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lowercase=True,
                     text_lemmatize=True, special_char_removal=True,
                     stop_words_removal=True, remove_digits=True):
    
    # this is the list that will contain each document after the wrangling
    normalized_corpus = []
    
    for doc in corpus:
        
        # HTML stripping
        if html_stripping:
            doc = strip_html_tags(doc)
        
        # REMOVE ACCENTED CHARACTERS
        if accented_char_removal:
            # we first apply this function to the document
            # then we override the variable with a new value
            doc = remove_accented_chars(doc)
        
        # EXPAND CONTRACTION
        if contraction_expansion:
            # doc = expand_contractions(doc, contraction_mapping=CONTRACTION_MAP)
            doc = contractions.fix(doc)
        
        # LOWERCASE
        if text_lowercase:
            doc = doc.lower()
            
        # REMOVE EXTRA NWELINES
        # here we use regex \r --> carriage return, \n --> line feed
        doc = re.sub(r"[\r|\n|\r\n]+", ' ',doc)
        
        # LEMMATIZATION
        if text_lemmatize:
            doc = lemmatize(doc)
        
        # REMOVE SPECIAL CHARACTERS
        if special_char_removal:
            # insert spaces between special characters
            # special_char_pattern = re.compile(r'([{.(-)!}])') --> ORIGINAL
            special_char_pattern = re.compile(r'([{(-)}])')
            # this adds white space that is then removed
            doc = special_char_pattern.sub(" \\1 ",doc)
            doc = remove_special_character(doc, remove_digits=remove_digits)
        
        # REMOVE EXTRA WHITESPACE
        # doc = re.sub(r'\s+', ' ',text)
        doc = re.sub(' +', ' ',doc)
        
        # REMOVE STOPWORDS
        if stop_words_removal:
            doc = remove_stopwords(doc, is_text_lowercase=text_lowercase)
            
        # once we've cleaned the text we can add it to the list
        normalized_corpus.append(doc)
    return normalized_corpus