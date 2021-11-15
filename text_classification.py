social = set(['cats','cat','dogs','dog','house','ex', 'friendship','relationship','relationships','sex','covid',
              'lockdown','shutdown', 'quarantine','school', 'talking',
              'college','job','jobs','work','colleague','colleagues','coworker','friend','friends','buddy', 
              'pal','play','he','his','him','she','her','parents','family','fam','cousin','mom', 'dad',
              'moms','dads','mother','mothers','father','fathers','son','brother','daughter','sister','sis',
              'sisters','brothers','kid','kids','partner','member',
              'boyfriend','bf','boy','boys','girlfriend','gf','girl','fiancé','fiance','fiancée','girls','man','woman',
              'fiancee','husband','doctor','doctors'
              ,'shrink','psychiatrist','psychiatrists','therapy','therapist','therapists','talk','group', 'loan'])

emotional = set(['positive','negative','thought','thoughts','misery','miserable','heal','healing','nice','recovering','recover','smile','purpose','helping','help','happy','happiness','love','loved','lovely','lovable','fine','ok','good','well','great','better','care',
                'amazing','awesome','try','fix','satisfied', 'powerless','fire','relieved',
                'gone','die', 'dying','severe','burden', 'harrassment','abuse', 'abusive',
                'broken','worthless','bad','stressful','stress','fuck','hate','hatred','upset','sad','sadness','loss',
                'mad','afraid','down','depressed','depression','anxious','anxiety','shit','shitty',
                'suicide','suicidal','intrusive', 'hopeless','fear','shame','guilt','scared',
                'guiltiness','self-hatred','self-pity','grief','waste','wasted',
                'dissatisfied','frustrated','frustrating','exhausting','powerless',
                'loneliness','lonely','cry','crying', 'awful','overwhelmed','overwhelming','hope','hopelessness'])


personal_words = ['i', 'me', 'my', 'myself','mine']
collective_words = ['we', 'us', 'ours', 'ourselves','they', 'their', 'them', '\'em', 'themselves']

stop_words = ['were','are','is','am','between','yourself','but','again','there','about','once', 'be',
              'during','out','very','have','having','with','own','an','some','for','its',
              'yours','such','into','of','most','itself','other','off','or', 'who','as',
              'from','each','the','until','below','these','your','through','did','do','does',
              'don','nor','more','himself','this','should','while','above','both','up',
              'to','had','she','all','no','when','at','any', 'before','same','and','been',
              'have','has','had','in','on','yourselves','then','that','because','what','over',
              'why','so','now','under','herself','just','where','too','only','which',
              'those','after','few','being','if','against','a','by','how','further',
              'here','than']


import nltk
from collections import Counter

def text_classifier(text):

    # tokenize text + remove stop words
    words = [word.lower() for word in nltk.word_tokenize(text)
             if word not in stop_words if word.isalpha()] # .isalpha --> alphabetical

    count = Counter(words).most_common()

    token_social = 0
    token_emotional = 0
    token_pronouns = 0
    token_collective = 0

    # count and add frequency to lists
    for token,freq in count:

        if token in social:
            token_social += freq
        elif token in emotional:
            token_emotional += freq
        elif token in personal_words:
            token_pronouns += freq
        elif token in collective_words:
            token_collective += freq
    #------------------------------------------------------------------# 
    # which social/emotional words?

    if token_social > 0 and token_emotional == 0:
        return 'social'

    elif token_social == 0 and token_emotional > 0:
        return 'emotional'

    elif token_social > 0 and token_emotional > 0:
        if token_emotional > token_social:
            return 'emotional and social'

        elif token_social > token_emotional:
            return 'social and emotional'

        elif token_social == token_emotional:
            return 'equal'

    else:
        return 'unknown'
