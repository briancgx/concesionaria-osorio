from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Aquí puedes agregar lógica de autenticación
        return f"Bienvenido {username}!"
    return render_template("login.html")
# Ruta principal

@app.route('/panel')
def panel_control():
    return render_template('panel_control.html')

@app.route('/clientes')
def clientes():
    # Aquí puedes obtener la lista de clientes desde la base de datos
    return render_template('clientes.html')

@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta templates/

if __name__ == '__main__':
    app.run(debug=True)
