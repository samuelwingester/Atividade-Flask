from flask import Flask, jsonify, request
from data import *

from library import Library

app = Flask(__name__)

@app.route('/')
def root():
    return ("ok", 200)

@app.route('/biblioteca', methods=['GET', "POST"])
@app.route('/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def Biblioteca(isbn=None):
    lib = Library()
    method = request.method

    if method == 'GET':
        if isbn:
            return lib.GetBook(isbn)
        else:
            return lib.GetList()

    elif method == 'POST':
        return lib.InsertBook()

    elif method == 'DELETE':
        return lib.DeleteBook(isbn)

    elif method == "PUT":
        return lib.UpdateBook(isbn)
    
    return jsonify({"message":"Requisição recusada"}), 503

if __name__ == "__main__":
    app.run(debug=True)
