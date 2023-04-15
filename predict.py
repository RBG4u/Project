from preprocessing import querying
from model import app
import joblib
from collections import Counter


def query_prepr_comments(number):
    while True:
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


def raw_text(number):
    prepr_tokens = query_prepr_comments(number)
    raw_text = [" ".join(tokens) for tokens in prepr_tokens]
    return raw_text


def predict(number):
    model = joblib.load('svm_model_3000.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    text = raw_text(number)
    vectors = vectorizer.transform(text)
    predict = model.predict(vectors)
    my_counter = Counter(predict)
    comments_count = len(predict)
    positive_count = my_counter[1]
    negative_count = my_counter[-1]
    positive_percentage = positive_count / (comments_count / 100)
    negative_percentage = negative_count / (comments_count / 100)
    return comments_count, positive_count, negative_count, positive_percentage, negative_percentage


if __name__ == '__main__':
    number = input('Группы: \n 1. Лентач\n 2. Фишмарт\n\nВведите номер группы: ')
    comments_count, positive_count, negative_count, positive_percentage, negative_percentage = predict(number)
    print(f"Процент положительных комментариев: {positive_percentage}")
    print(f"Процент отрицательных комментариев: {negative_percentage}")