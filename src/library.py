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
    
    def GetRequestData(self):
        #Verifica o formato dos dados passados na requisição e normaliza para dict
        if request.is_json: 
            #JSON
            return request.get_json()

        elif request.content_type == 'application/x-www-form-urlencoded': 
            #FORM
            return request.form.to_dict()
        
        return None

    def GetList(self):
        return render_template('base.html', data=self.data), 200

    def GetBook(self, isbn):
        book = self.FindBook(isbn)
        if book is None: 
            return jsonify({"message":"Recurso nao localizado"}), 404
        return jsonify(book), 200

    def InsertBook(self):
        book = self.GetRequestData()

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
        newbook = self.GetRequestData()

        if newbook != None:
            index = self.FindIndex(isbn)

            if index is None:
                return jsonify({"message":"Recurso nao localizado"}), 404

            for key, value in newbook.items():
                self.data[index][key] = value

            Data().save(self.data)

            return redirect(url_for('Biblioteca'))
        
        return redirect(url_for('BibliotecaAtualizar'))
