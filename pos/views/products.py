from flask import Blueprint, render_template, redirect, request, abort
from pos.models import db
from pos.models.products import Products

bp = Blueprint("products", __name__)

@bp.route("/products")
def products_list():
	products = Products.query.all()
	return render_template("products/list.html", products=products)


@bp.route("/products/add", methods=["POST", "GET"])
def products_add():
	if request.method == 'GET':
		return render_template("products/form_add.html")

	name = request.form['name']
	price = request.form['price']
	stock = request.form['stock']

	product = Products()
	product.name = name
	product.price = price
	product.stock = stock

	db.session.add(product)
	db.session.commit()

	return redirect("/products")


@bp.route("/products/update", methods=["POST", "GET"])
def product_update():
	if request.method == "GET":
		# get products by id
		product_id = request.args['id']
		product = Products.query.filter_by(id=product_id).first()
		if not product:
			abort(404)
		return render_template('products/form_edit.html', product=product)

	product_id = request.args['id']
	name = request.form['name']
	price = request.form['price']
	stock = request.form['stock']

	# get product by id
	product = Products.query.filter_by(id=product_id).first()
	if not product:
		abort(404)

	# update product
	product.name = name
	product.price = price
	product.stock = stock

	db.session.add(product)
	db.session.commit()

	return redirect("/products")


@bp.route("/products/delete")
def product_delete():
    """Delete product"""
    product_id = request.args['id']
    product = Products.query.filter_by(id=product_id).first()
    if product:
        # delete product by id
        db.session.delete(product)
        db.session.commit()

    return redirect("/products")