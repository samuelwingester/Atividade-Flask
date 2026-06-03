from data import carregar_do_arquivo, salvar_no_arquivo

from flask import jsonify, request, render_template

class Library:
    
    data = None

    def __init__(self):
        self.data = carregar_do_arquivo()

    def FindBook(self, isbn):
        for i in range(len(self.data)):
            if self.data[i]["isbn"] == isbn:
                return self.data[i]
        return None

    def FindIndex(self, isbn):
        for i in range(len(self.data)):
            if self.data[i]["isbn"] == isbn:
                return i
        return None

    def GetList(self):
        return render_template('biblioteca.html', data=self.data), 200

    def GetBook(self, isbn):
        book = self.FindBook(isbn)
        if book is None: 
            return jsonify({"message":"Recurso nao localizado"}), 404
        return jsonify(book), 200

    def InsertBook(self):
        if request.is_json:
            book = request.get_json()
            self.data.append(book)
            salvar_no_arquivo(self.data)

            return jsonify({"message":"Recurso criado com sucesso"}), 201

        return jsonify({"message":"erro ao criar recurso"}), 400

    def DeleteBook(self, isbn):
        index = self.FindIndex(isbn)

        if index is None:
            return jsonify({"message":"Recurso nao localizado"}), 404

        self.data.pop(index)
        salvar_no_arquivo(self.data)

        return jsonify({"message":"Recuro deletado com sucesso"}), 200

    def UpdateBook(self, isbn):
        newinfo = request.get_json()
        index = self.FindIndex(isbn)

        if index is None:
            return jsonify({"message":"Recurso nao localizado"}), 404

        for key, value in newinfo.items():
            self.data[index][key] = value

        salvar_no_arquivo(self.data)

        return jsonify({"message":"Recuro atualizado com sucesso"}), 200
