import tweepy
from tweepy import OAuthHandler, Cursor
import pandas as pd
import nltk
from nltk import word_tokenize
import string
import numpy as np
from unidecode import unidecode
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine

nltk.download('stopwords')
nltk.download('punkt')
nlp = spacy.load('pt_core_news_sm')

twitter_keys = {
    'consumer_key': 'DGmtRmEYnl1e9cDo0DKpqyoX6',
    'consumer_secret': 'MO1Z9Ymo5DFmUbbMIGOwFeQusCfhPGgYiDX59h6E4yE9cOiaRU',
    'access_token_key': '2340259878-xTkziDtbm5OPlB0SGlQO9N7yZ1mMHNgdGf0Sxn0',
    'access_token_secret': 'ZlUey81CQcYem9htqyGw9S6s6kV32oZ34MK7bAnLbcg32'
}


def tweepy_config(twitter_keys):
    """'
    Instanciando a configuracao da API twiiter

    twitter_keys: chaves de acesso
    api: instancia api
    """

    auth = OAuthHandler(twitter_keys['consumer_key'],
                        twitter_keys['consumer_secret'])
    auth.set_access_token(twitter_keys['access_token_key'],
                          twitter_keys['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=False)

    return api


def tweets_scrapy(api):
    """'
    Coleta dos dados no twitter (#Formula1, em portugues, sem retweets e links)

    api: instancia da API configurada
    df: dataframe com as variaveis coletadas
    """

    search = tweepy.Cursor(api.search_tweets,
                           q='formula 1 -filter:retweets -filter:links lang:pt',
                           tweet_mode='extended').items(10)
    tweets = []
    for item in search:
        tweet = {'created_at': item.created_at, 'text': item.full_text}
        tweets.append(tweet)
    df = pd.DataFrame.from_records(tweets)

    return df


def normalize(df_twt):
    """'
    Normalizacao dos dados: stopwords, lowercase e unidecode

    df_twt: dataframe com os tweets coletados
    df_twt['processed']: coluna do dataframe que passou por normalizacao
    """

    stopwords = nltk.corpus.stopwords.words('portuguese')
    palavras_extras = ['pra', 'pro', 'pq', 'https']
    stopwords = np.concatenate([stopwords, palavras_extras, list(string.punctuation)])

    df_twt['processed'] = df_twt.apply(lambda row: ' '.join(
        w for w in [unidecode(word.lower()) for word in word_tokenize(row.text)] if not w.lower() in stopwords), axis=1)

    return df_twt['processed']


def lemanization(sentence):
    """'
    Lemanizacao dos dados normalizados: Reduz o token ao lema
z
    sentence: lista de dados normalizados
    """

    sentence_tokenize = [token.lemma_ for token in nlp(sentence.lower())
                         if (token.is_alpha & ~token.is_stop)]
    return ' '.join(sentence_tokenize)


def tfidf_processing(sentences, gram):
    """'
    Aplicacao da tecnica TF-IDF para encontrar as palavras mais relevantes
    e seus respectivos pesos no corpus

    Criacao do dataframe com o bigrama ou trigrama (encontrado em features_name)
    e seu respectivo rank (soma dos pesos TF-IDF)
    """

    preprocessed_sentences = [lemanization(sentence) for sentence in sentences]
    vec_tdidf = TfidfVectorizer(ngram_range=(gram, gram))
    tfidf = vec_tdidf.fit_transform(preprocessed_sentences)
    features = vec_tdidf.get_feature_names()

    soma = tfidf.sum(axis=0)
    df_final = []

    for col, term in enumerate(features):
        df_final.append((term, soma[0, col]))
    ranking = pd.DataFrame(df_final, columns=['termo', 'rank'])
    df_rankeado = (ranking.sort_values('rank', ascending=False))

    return df_rankeado


def to_sqlite(df, name):
    """'
    Insercao dos dados no SQLite com determinado nome (bigrama ou trigrama)
    """

    db = create_engine(f'sqlite:///twitter_{name}.sqlite', echo=False)
    conn = db.connect()

    schema = f'''
    CREATE TABLE twitter_{name}(
        termo                TEXT,
        rank                 REAL
    )
    '''

    conn.execute(schema)
    df.to_sql(f'twitter_{name}', con=conn, if_exists='append', index=False)


if __name__ == '__main__':
    df_initial = tweets_scrapy(tweepy_config(twitter_keys))
    df_normalized = normalize(df_initial)
    df_ranked_bi = tfidf_processing(df_normalized, 2)
    df_ranked_tri = tfidf_processing(df_normalized, 3)

    print(len(df_ranked_bi))
    print(df_ranked_bi.head())
    print('==========\n\n\n')
    print(len(df_ranked_tri))
    print(df_ranked_tri.head())

    to_sqlite(df_ranked_bi, 'bigram')
    to_sqlite(df_ranked_tri, 'trigram')
