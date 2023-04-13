from preprocessing import querying
from model import app
import joblib
from collections import Counter


def query_prepr_comments():
    while True:
        number = input('Группы: \n 1. Лентач\n 2. Фишмарт\n\nВведите номер группы:')
        if number == '1':
            id_group = '29534144'
            break
        elif number == '2':
            id_group = '26464472'
            break
        else:
            print('\nТакого номера группы пока нет(\n')
    with app.app_context():
        prepr_tokens = querying(id_group)
    return prepr_tokens


def raw_text():
    prepr_tokens = query_prepr_comments()
    raw_text = [" ".join(tokens) for tokens in prepr_tokens]
    return raw_text


def predict():
    model = joblib.load('svm_model_3000.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    text = raw_text()
    vectors = vectorizer.transform(text)
    predict = model.predict(vectors)
    my_counter = Counter(predict)
    comments_count = len(predict)
    positive_count = my_counter[1]
    negative_count = my_counter[-1]
    return comments_count, positive_count, negative_count


if __name__ == '__main__':
    comments_count, positive_count, negative_count = predict()
    print(f"Процент положительных комментариев: {positive_count/(comments_count/100)}")
    print(f"Процент отрицательных комментариев: {negative_count/(comments_count/100)}")