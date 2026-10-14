from flask import Flask, render_template, request
from smart_calculator import calculate

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    expression = ""
    result = ""

    if request.method == "POST":
        expression = request.form.get("expression", "").strip()

        if expression:
            result = calculate(expression)

    return render_template(
        "index.html",
        expression=expression,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
