import shopify

API_KEY = '<api-key>'
PASSWORD = '<password>'
SHOP_NAME = '<shop-name>'

shop_url = f'https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin'
shopify.ShopifyResource.set_site(shop_url)

# Get a list of all orders
orders = shopify.Order.find()

for order in orders:
  if order.fulfillment_status is None:
    # Fulfill the order
    fulfillment = shopify.Fulfillment({'order_id': order.id, 'line_items': [{'id': line_item.id} for line_item in order.line_items]})
    fulfillment.save()
    print(f'Order {order.id} fulfilled')