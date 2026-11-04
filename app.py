from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "local-development-only"

@app.route("/")
def main():
    return render_template("main.html", products=[])

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/reg_items")
def register_product():
    return render_template("register_product.html")

if __name__ == "__main__":
    app.run(debug=True)
