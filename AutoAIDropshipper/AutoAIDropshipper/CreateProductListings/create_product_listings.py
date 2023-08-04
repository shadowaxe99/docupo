import openai

openai.api_key = '<openai_api_key>'

# Define the product details
product_details = {
    'name': 'iPhone Charger',
    'description': 'A high-quality iPhone charger that supports fast charging.',
    'image': 'https://www.example.com/images/iphone_charger.jpg'
}

# Generate the product title
product_title = openai.Completion.create(
    engine='text-davinci-003',
    prompt=f'Generate a catchy title for a product with the following details: {product_details}',
    max_tokens=64
).choices[0].text.strip()

# Generate the product description
product_description = openai.Completion.create(
    engine='text-davinci-003',
    prompt=f'Generate a detailed description for a product with the following details: {product_details}',
    max_tokens=256
).choices[0].text.strip()

# Print the generated product title and description
print(f'Product Title: {product_title}')
print(f'Product Description: {product_description}')