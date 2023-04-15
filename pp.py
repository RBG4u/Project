import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import re
from querying_comment import query_comment
from model import app
from multiprocessing import Pool
from joblib import Parallel, delayed
from tqdm import tqdm


def querying(id_group):
    comments = query_comment(id_group)
    preprocessed_comments_text = []
    for comment in comments:
        text = comment['text']
        if text == '':
            continue
        preprocessed_comment = ''.join(preprocessing(text))
        if preprocessed_comment == []:
            continue
        preprocessed_comments_text.append(preprocessed_comment)
    lemm_text = join(preprocessed_comments_text)
    return lemm_text


def preprocessing(comment):
    regular_comment_text = []
    text = remove_url(comment)
    text = remove_tags(text)
    text = remove_username(text)
    text = remove_id(text)
    text = remove_punct_numbers(text)
    text = lowercase_text(text)
    #text = tokens_lemmatize(text)
    #tokens = tokenize_words(text)
    #tokens = remove_stopwords(tokens)
    #tokens = tokens_lemmatize_2(tokens)
    #tokens = tokens_stemmer(tokens)
    #tokens = removing_short_tokens(tokens)
    if text != '':
        regular_comment_text.extend(text)
    return regular_comment_text


def join(text):
    text_string = '. '.join(text)
    preprocessed_comment_text = []
    lemmatizer = Mystem()
    lemmatized_string = Parallel(n_jobs=-1)(delayed(tokens_lemmatize)(t, lemmatizer) for t in tqdm(text_string))
    lemmatized_sentences = lemmatized_string.split('.')
    for sentence in lemmatized_sentences:
        tokens = tokenize_words(sentence)
        tokens = remove_stopwords(tokens)
        tokens = removing_short_tokens(tokens)
        if tokens != []:
            preprocessed_comment_text.extend(tokens)
    return preprocessed_comment_text


def remove_url(text):
    text = re.sub(r'https?://\S+', '', text)
    return text


def remove_tags(text):
    text = re.sub(r'#\S+', '', text)
    return text


def remove_username(text):
    text = re.sub(r'@\S+', '', text)
    return text


def remove_id(text):
    text = re.sub(r'id', '', text)
    return text


def remove_punct_numbers(text):
    text = re.sub(r'[^\w\s]|[\d]', '', text)
    return text


def lowercase_text(text):
    text = text.lower()
    return text


def tokenize_words(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words('russian'))
    tokens = [token for token in tokens if not token in stop_words]
    return tokens


def tokens_lemmatize(tokens, lemmatizer):
    #lemmatizer = Mystem()
    tokens = [lemmatizer.lemmatize(tokens)]
    return tokens


def tokens_lemmatize_2(tokens, cores=6):
    with Pool(processes=cores) as pool:
        lemmatizer = pymystem3.Mystem(entire_input=False)
        tokens = pool.map(lemmatizer.lemmatize, tokens)
    return tokens


def tokens_stemmer(tokens):
    stemmer = RussianStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


def removing_short_tokens(tokens):
    tokens = [token for token in tokens if len(token) > 2]
    return tokens


if __name__ == '__main__':
    with app.app_context():
        id_group = '26464472'
        pp = querying(id_group)
        print(type(pp))
        print(1)