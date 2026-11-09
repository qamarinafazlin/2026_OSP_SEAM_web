from flask import Flask, render_template, request, abort, session, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "local-development-only"


# =====================================================================
# TEMPORARY SAMPLE DATA (for previewing the frontend)
# The backend will replace these two lists with data from Firebase.
# =====================================================================

PRODUCTS = [
    {"id": 1, "name": "Mamee Monster Noodle Snack", "country": "Malaysia", "status": "On sale",
     "price": 2500, "seller": "ewha_amira", "pickup": "ECC B4, near the main entrance",
     "listed_date": "2026-10-03", "image_url": "", "extra_images": [],
     "description": "The crunchy noodle snack every Malaysian kid grew up with. "
                    "Eat it straight from the pack or sprinkle the seasoning on top."},
    {"id": 2, "name": "Super Ring", "country": "Malaysia", "status": "On sale",
     "price": 3000, "seller": "ewha_amira", "pickup": "Student Union, 1F",
     "listed_date": "2026-10-05", "image_url": "", "extra_images": [],
     "description": "Cheesy ring-shaped corn snack. Very addictive."},
    {"id": 3, "name": "Tamarind Flakes", "country": "Myanmar", "status": "Reserved",
     "price": 2000, "seller": "thiri_k", "pickup": "Engineering Building A",
     "listed_date": "2026-10-07", "image_url": "", "extra_images": [],
     "description": "Sweet and sour tamarind discs, a classic from Myanmar."},
    {"id": 4, "name": "Aarul (dried curd)", "country": "Mongolia", "status": "On sale",
     "price": 5000, "seller": "bolor_m", "pickup": "Library entrance",
     "listed_date": "2026-10-08", "image_url": "", "extra_images": [],
     "description": "Traditional dried curd. Firm, tangy, and good for long study nights."},
    {"id": 5, "name": "Mongolian Chocolate", "country": "Mongolia", "status": "Sold out",
     "price": 4000, "seller": "bolor_m", "pickup": "Library entrance",
     "listed_date": "2026-10-09", "image_url": "", "extra_images": [],
     "description": "Sweet chocolate from Ulaanbaatar. Goes well with tea."},
]

REVIEWS = [
    {"id": 1, "title": "Tastes exactly like childhood", "product_name": "Mamee Monster Noodle Snack",
     "price": "2,500", "rating": 5, "reviewer_id": "hana_kim", "date": "2026-10-04", "image": "", "color": "#E9C949",
     "content": "My Malaysian friend used to bring these back after every break, so I was very happy to find them here.\n"
                "Crunchy, salty and the seasoning packet is the best part!!\n"
                "Picked it up at ECC. Bought three and am already regretting not buying ten."},
    {"id": 2, "title": "Sour, chewy, addictive", "product_name": "Tamarind Flakes",
     "price": "2,000", "rating": 3, "reviewer_id": "sarakim", "date": "2026-10-09", "image": "", "color": "#E56869",
     "content": "Sweet-sour little discs. Great for late-night study sessions in the library."},
    {"id": 3, "title": "Harder than I expected", "product_name": "Aarul (dried curd)",
     "price": "5,000", "rating": 3, "reviewer_id": "minseoJ", "date": "2026-10-03", "image": "", "color": "#4D98E7",
     "content": "Very firm and tangy. The seller told me to let it soften slowly -- good tip."},
    {"id": 4, "title": "Great with ramyeon", "product_name": "Mamee Monster Noodle Snack",
     "price": "2,500", "rating": 4, "reviewer_id": "soyeon22", "date": "2026-10-02", "image": "", "color": "#E9C949",
     "content": "Crushed it over cup noodles. Would recommend to anyone who likes snacks with crunch."},
    {"id": 5, "title": "So delicious!", "product_name": "Super Ring",
     "price": "3,000", "rating": 5, "reviewer_id": "student01", "date": "2026-10-11", "image": "", "color": "#E9C949",
     "content": "Cheesy and crunchy. I really enjoyed it!"},
    {"id": 6, "title": "Perfect sweet snack", "product_name": "Mongolian Chocolate",
     "price": "4,000", "rating": 4, "reviewer_id": "student02", "date": "2026-10-12", "image": "", "color": "#E56869",
     "content": "Sweet and delicious with tea."},
    {"id": 7, "title": "Interesting flavor", "product_name": "Traditional Snack",
     "price": "3,500", "rating": 4, "reviewer_id": "student03", "date": "2026-10-13", "image": "", "color": "#4D98E7",
     "content": "A unique taste. I would try it again."},
    {"id": 8, "title": "My new favorite", "product_name": "Crispy Noodles",
     "price": "3,500", "rating": 5, "reviewer_id": "student04", "date": "2026-10-14", "image": "", "color": "#E9C949",
     "content": "Very crunchy and flavorful!"},
]


def find_product_by_name(name):
    return next((p for p in PRODUCTS if p["name"] == name), None)


# =====================================================================
# PRODUCTS
# =====================================================================

@app.route("/")
def main():
    page = request.args.get("page", 1, type=int)
    per_page = 8
    total_pages = max(1, (len(PRODUCTS) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    return render_template(
        "main.html",
        products=PRODUCTS[start:start + per_page],
        page=page,
        total_pages=total_pages
    )


@app.route("/view_detail/<int:product_id>")
def view_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        abort(404)

    reviews = [r for r in REVIEWS if r["product_name"] == product["name"]]
    if reviews:
        avg = sum(r["rating"] for r in reviews) / len(reviews)
        product = dict(product, rating=round(avg, 1))

    return render_template("product_detail.html", product=product, reviews=reviews)


@app.route("/reg_items")
def register_product():
    return render_template("register_product.html")


# =====================================================================
# REVIEWS
# =====================================================================

@app.route("/review")
def review_list():
    page = request.args.get("page", 1, type=int)
    per_page = 4
    total_pages = max(1, (len(REVIEWS) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    return render_template(
        "review_list.html",
        reviews=REVIEWS[start:start + per_page],
        total_reviews=len(REVIEWS),
        page=page,
        total_pages=total_pages
    )


@app.route("/review/<int:review_id>")
def review_detail(review_id):
    review = next((r for r in REVIEWS if r["id"] == review_id), None)
    if review is None:
        abort(404)

    # link "View product" to the right product page (if that product exists)
    product = find_product_by_name(review["product_name"])
    review = dict(review, product_id=product["id"] if product else None)

    return render_template("review_detail.html", review=review)


@app.route("/reg_review")
def write_review():
    return render_template("write_review.html")


# =====================================================================
# ACCOUNTS
# =====================================================================

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# TEMPORARY: lets you preview the logged-in header. Delete when real login works.
@app.route("/test_login")
def test_login():
    session["id"] = "nina"
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)