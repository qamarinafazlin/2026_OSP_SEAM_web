from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "local-development-only"

@app.route("/")
def main():
    return render_template("main.html", products=[])

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/reg_items")
def register_product():
    return render_template("register_product.html")


@app.route("/review")
def review_list():
    from flask import request

    reviews = [
        {
            "id": 1,
            "title": "Tastes exactly like childhood",
            "product_name": "Mamee Monster Noodle Snack",
            "rating": 5,
            "content": "Crunchy, salty, and the seasoning packet is the best part. Bought three.",
            "reviewer_id": "hana_kim",
            "date": "2026-10-04",
            "image": "",
            "color": "#E9C949"
        },
        {
            "id": 2,
            "title": "Sour, chewy, addictive",
            "product_name": "Tamarind Flakes",
            "rating": 3,
            "content": "Sweet-sour little discs. Great for late-night study sessions in the library.",
            "reviewer_id": "sarakim",
            "date": "2026-10-09",
            "image": "",
            "color": "#E56869"
        },
        {
            "id": 3,
            "title": "Harder than I expected",
            "product_name": "Aarul (dried curd)",
            "rating": 3,
            "content": "Very firm and tangy. The seller told me to let it soften slowly -- good tip.",
            "reviewer_id": "minseoJ",
            "date": "2026-10-03",
            "image": "",
            "color": "#4D98E7"
        },
        {
            "id": 4,
            "title": "Great with ramyeon",
            "product_name": "Mamee Monster Noodle Snack",
            "rating": 4,
            "content": "Crushed it over cup noodles. Would recommend to anyone who likes snacks with crunch.",
            "reviewer_id": "soyeon22",
            "date": "2026-10-02",
            "image": "",
            "color": "#E9C949"
        },
        {
            "id": 5,
            "title": "So delicious!",
            "product_name": "Super Ring",
            "rating": 5,
            "content": "Cheesy and crunchy. I really enjoyed it!",
            "reviewer_id": "student01",
            "date": "2026-10-11",
            "image": "",
            "color": "#E9C949"
        },
        {
            "id": 6,
            "title": "Perfect sweet snack",
            "product_name": "Mongolian Chocolate",
            "rating": 4,
            "content": "Sweet and delicious with tea.",
            "reviewer_id": "student02",
            "date": "2026-10-12",
            "image": "",
            "color": "#E56869"
        },
        {
            "id": 7,
            "title": "Interesting flavor",
            "product_name": "Traditional Snack",
            "rating": 4,
            "content": "A unique taste. I would try it again.",
            "reviewer_id": "student03",
            "date": "2026-10-13",
            "image": "",
            "color": "#4D98E7"
        },
        {
            "id": 8,
            "title": "My new favorite",
            "product_name": "Crispy Noodles",
            "rating": 5,
            "content": "Very crunchy and flavorful!",
            "reviewer_id": "student04",
            "date": "2026-10-14",
            "image": "",
            "color": "#E9C949"
        }
    ]

    page = request.args.get("page", 1, type=int)
    per_page = 4
    total_pages = (len(reviews) + per_page - 1) // per_page

    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    visible_reviews = reviews[start:start + per_page]

    return render_template(
        "review_list.html",
        reviews=visible_reviews,
        total_reviews=len(reviews),
        page=page,
        total_pages=total_pages
    )



@app.route("/review/<int:review_id>")
def review_detail(review_id):
    from flask import abort

    # Temporary example data for frontend testing
    reviews = {
        1: {
            "title": "Tastes exactly like childhood",
            "rating": 5,
            "reviewer_id": "hana_kim",
            "date": "2026-10-04",
            "content": (
                "My Malaysian friend used to bring these back after every break, "
                "so I was very happy to find them here.\n"
                "Crunchy, salty and the seasoning packet is the best part!!\n"
                "Picked it up at ECC. Bought three and am already regretting not buying ten."
            ),
            "product_name": "Mamee Monster noodle snack",
            "price": "2,500",
            "product_id": None,
            "image": ""
        }
    }

    review = reviews.get(review_id)

    if review is None:
        abort(404)

    return render_template("review_detail.html", review=review)

@app.route("/reg_review", methods=["GET"])
def write_review():
    return render_template("write_review.html")

if __name__ == "__main__":
    app.run(debug=True)
