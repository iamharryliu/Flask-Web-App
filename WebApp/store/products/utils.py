from WebApp.models import Product

# Read


def get_all_products():
    products = Product.query.all()
    return products


def get_product(id):
    product = Product.query.get_or_404(id)
    return product


def search_products(search):
    products = Product.query.filter(
        Product.name.like(f"%{search}%")
        | Product.description.like(f"%{search}%")
        | Product.color.like(f"%{search}%")
        | Product.description.like(f"%{search}%")
        | Product.code.like(f"%{search}%")
    )
    return products

