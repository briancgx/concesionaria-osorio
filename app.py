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
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta templates/

if __name__ == '__main__':
    app.run(debug=True)
