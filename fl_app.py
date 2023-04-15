from model import app
import joblib
import numpy as np
from predict import predict
from flask import Flask, request, render_template, jsonify
from preprocessing import preprocessing


@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html')


@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    number = request.form['name']

    comments_count, positive_count, negative_count, positive_percentage, negative_percentage = predict(number)

    return jsonify({
        "comments_count": comments_count,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage
    })


@app.route('/analyze_text', methods=['POST'])
def analyze_sentiment_text():
    text = request.form['name2']
    model = joblib.load('svm_model_3000.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    text = preprocessing(text)
    raw_text = [" ".join(text)]
    vectors = vectorizer.transform(raw_text)
    predict = model.predict(vectors)
    string_predict = np.array_str(predict)
    if string_predict == '[1]':
        result = 'положительный'
    elif string_predict == '[-1]':
        result = 'отрицательный'
    else:
        result = string_predict

    return jsonify({
        "result": result
    })


if __name__ == '__main__':
    app.run(debug=False)