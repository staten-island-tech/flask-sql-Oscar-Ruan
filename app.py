from flask import Flask, render_template, request, redirect, url_for, abort
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://www.fruityvice.com/api/fruit/all")
    data = response.json()
    fruit_list = data

    fruits = []

    for fruit in fruit_list:
        fruits.append({
            'name': fruit['name'].capitalize(),
            'id': fruit['id']
        })
    
    fruits.sort(key=lambda f: f['id'])

    return render_template("index.html", fruits=fruits)


@app.route("/fruit/<int:id>")
def fruity_detail(id):
    
    try:
        response = requests.get(f"https://www.fruityvice.com/api/fruit/{id}")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        abort(404)

    name = data.get('name').capitalize()
    fruit_id = data.get('id')
    family = data.get('family')
    order = data.get('order')
    genus = data.get('genus')

    fruit_names = []
    fruit_value = []

    for key, values in data['nutritions'].items():
        fruit_names.append(key)
        fruit_value.append(values)

    nutrition = zip(fruit_names, fruit_value)

    return render_template("fruits.html", fruit={
        'name': name,
        'id': fruit_id,
        'family': family,
        'order': order,
        'genus': genus,
        'nutrition': nutrition
    })


@app.route("/search")
def search_by_id():
    fruit_id = request.args.get("fruit_id", type=int)
    if fruit_id is None:
        return redirect(url_for("index"))
    return redirect(url_for("fruity_detail", id=fruit_id))

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.route("/book", methods=["POST"])
def book_fruit():
    fruit_id = request.form.get("fruit_id", type=int)
    quantity = request.form.get("quantity", type=int)
    name = request.form.get("name", type=str)

    if not fruit_id or not quantity:
        abort(400)

    try:
        response = requests.get(f"https://www.fruityvice.com/api/fruit/{fruit_id}")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        abort(404)

    fruit_name = data.get('name').capitalize()

    return render_template("booking.html", fruit_name=fruit_name, quantity=quantity, name=name)

if __name__ == '__main__':
    app.run(debug=True)