import shopify

# Create a new session
session = shopify.Session('<my-shopify-url>', '2022-04', '<access-token>')

# Activate the session
shopify.ShopifyResource.activate_session(session)

# Create a new product
new_product = shopify.Product()
new_product.title = 'My New Product'
new_product.product_type = 'Clothing'
new_product.vendor = 'John Doe'
new_product.save()

# Deactivate the session when you're done
shopify.ShopifyResource.clear_session()