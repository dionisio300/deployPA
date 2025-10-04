from flask import Flask, render_template, request, url_for
import mysql.connector as my
import os
import dotenv

dotenv.load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
host = os.getenv('HOST')

def conectarBanco():
    conexao = my.connect(
        user=user,
        password=password,
        database=database,
        host=host
    )
    return conexao


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    titulo = 'Página Inicial'
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        print(f'Email: {email}, Senha: {senha}')

        conexao = conectarBanco()
        cursor = conexao.cursor(dictionary=True)
        sql = 'select * from usuarios where email = %s'
        cursor.execute(sql,(email,))
        resultado = cursor.fetchone()
        print(resultado)

        if resultado:
            if senha == resultado['senha']:
                if resultado['tipo'] == 'cliente':
                    return render_template('cliente.html', usuario=resultado)
                elif resultado['tipo'] == 'admin':
                    return render_template('admin.html', usuario=resultado)
            else:
                print('senha Incorreta')

        else:
            print('Errou o email')
            return render_template('index.html',titulo=titulo)



        return render_template('index.html',titulo=titulo)


    return render_template('index.html',titulo=titulo)


if __name__ == '__main__':
    app.run(debug=True)

