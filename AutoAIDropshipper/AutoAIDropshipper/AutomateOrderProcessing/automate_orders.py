import shopify

# Create a new session
session = shopify.Session('<my-shopify-store>', '2022-04', '<access-token>')

# Activate the session
shopify.ShopifyResource.activate_session(session)

# Get a list of all orders
orders = shopify.Order.find()

# For each order, if it is not fulfilled, fulfill it
for order in orders:
    if not order.fulfillment_status:
        fulfillment = shopify.Fulfillment({'order_id': order.id, 'line_items': [{'id': line_item.id} for line_item in order.line_items]})
        fulfillment.save()

# Deactivate the session
shopify.ShopifyResource.clear_session()