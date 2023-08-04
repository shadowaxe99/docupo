import openai
import shopify

# Set the OpenAI API key
openai.api_key = '<openai_api_key>'

# Create a new session
session = shopify.Session('<my-shopify-store>', '2022-04', '<access-token>')

# Activate the session
shopify.ShopifyResource.activate_session(session)

# Get a list of all products
products = shopify.Product.find()

# For each product, generate a title and description using GPT-3
for product in products:
    title_prompt = f'Generate a catchy title for a product that is {product.title}.'
    description_prompt = f'Write a compelling product description for a {product.title}.'

    title_response = openai.Completion.create(engine='text-davinci-003', prompt=title_prompt, max_tokens=10)
    description_response = openai.Completion.create(engine='text-davinci-003', prompt=description_prompt, max_tokens=100)

    product.title = title_response.choices[0].text.strip()
    product.body_html = description_response.choices[0].text.strip()
    product.save()

# Deactivate the session
shopify.ShopifyResource.clear_session()