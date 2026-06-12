from data import Data

from flask import jsonify, request, render_template, redirect, url_for

class Library:
    
    data = None

    def __init__(self):
        self.data = Data().load()

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
        return render_template('base.html', data=self.data), 200

    def GetBook(self, isbn):
        book = self.FindBook(isbn)
        if book is None: 
            return jsonify({"message":"Recurso nao localizado"}), 404
        return jsonify(book), 200

    def InsertBook(self):
        book = None

        if request.is_json: 
            book = request.get_json()

        elif request.content_type == 'application/x-www-form-urlencoded': 
            book = request.form.to_dict()

        if book != None:
            self.data.append(book)
            Data().save(self.data)

            return redirect(url_for('Biblioteca'))
        
        return redirect(url_for('BibliotecaCriar'))

    def DeleteBook(self, isbn):
        index = self.FindIndex(isbn)

        if index is None:
            return {"message":"Recurso nao localizado"}, 404

        self.data.pop(index)
        Data().save(self.data)

        return {"message":"Recuro deletado com sucesso"}, 200

    def UpdateBook(self, isbn):
        newinfo = request.get_json()
        index = self.FindIndex(isbn)

        if index is None:
            return jsonify({"message":"Recurso nao localizado"}), 404

        for key, value in newinfo.items():
            self.data[index][key] = value

        Data().save(self.data)

        return jsonify({"message":"Recuro atualizado com sucesso"}), 200
