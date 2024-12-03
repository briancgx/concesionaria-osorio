from flask import Flask, render_template, request, redirect, url_for  # Agrega request y redirect


app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Usuario: {username}, Contraseña: {password}")  # Agrega esta línea para depurar

        # Aquí puedes agregar la lógica de autenticación, por ejemplo, comparar con una base de datos.
        if username == "admin" and password == "password123":
            return redirect(url_for('dashboard'))  # Redirige a un panel de control si el login es exitoso.
        else:
            error = "Usuario o contraseña incorrectos."
            return render_template('login.html', error=error)

    return render_template('login.html')


# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta templates/

if __name__ == '__main__':
    app.run(debug=True)
