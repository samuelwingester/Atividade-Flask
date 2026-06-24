from flask import Flask, jsonify, request, render_template, redirect, url_for

from library import Library

app = Flask(__name__)
app.config["SECRET_KEY"] = "asojfcb9862qr47v"

@app.route('/')
def root():
    return redirect(url_for('Biblioteca'))

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

@app.route('/biblioteca/criar', methods=['GET'])
def BibliotecaCriar():
    return render_template('create.html'), 200

@app.route('/biblioteca/deletar/<isbn>', methods=['POST'])
def BibliotecaDeletar(isbn):
    lib = Library()

    status = lib.DeleteBook(isbn)

    redirect(url_for('Biblioteca'))

@app.route('/biblioteca/atualizar/<isbn>', methods=['POST', 'GET'])
def BibliotecaAtualizar(isbn):
    lib = Library()
    method = request.method

    if method == 'GET':
        book = lib.FindBook(isbn)
        if book != None:
            return render_template('update.html', data=book), 200
        return jsonify({"message":"Recurso nao localizado"}), 404

    else:
        return lib.UpdateBook(isbn)

if __name__ == "__main__":
    app.run(debug=True)
