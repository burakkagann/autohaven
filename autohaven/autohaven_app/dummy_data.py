# Dummy user data for testing
dummy_user_regular = {
    'group': 'regular',
    'name': 'Regular',
    'surname': 'User',
    'username': 'regularuser',
    'email': 'regular@example.com',
}

dummy_user_seller = {
    'group': 'seller',
    'name': 'Seller',
    'surname': 'User',
    'username': 'selleruser',
    'email': 'seller@example.com',
    'company_name': 'Seller Company',
}


# Dummy listings, orders, and offers data
dummy_listings = [
    {'task': 'Example Task 1', 'title': 'Example Title 1', 'price': 100, 'date': '27 June', 'status': 'Available'},
    {'task': 'Example Task 2', 'title': 'Example Title 2', 'price': 200, 'date': '28 June', 'status': 'Available'},
    {'task': 'Example Task 3', 'title': 'Example Title 3', 'price': 300, 'date': '29 June', 'status': 'Sold'},
]

dummy_orders = [
    {'task': 'Example Task 1', 'title': 'Example Title 1', 'listing': 'A1B2C3D4E', 'price': 100, 'date': '27 June', 'status': 'Accepted'},
    {'task': 'Example Task 2', 'title': 'Example Title 2', 'listing': 'F5G6H7I8J', 'price': 200, 'date': '28 June', 'status': 'Declined'},
    {'task': 'Example Task 3', 'title': 'Example Title 3', 'listing': 'K9L0M1N2O', 'price': 300, 'date': '29 June', 'status': 'Accepted'},
]

dummy_offers = [
    {'task': 'Example Task 1', 'title': 'Example Title 1', 'listing': 'A1B2C3D4E', 'price': 100, 'date': '27 June'},
    {'task': 'Example Task 2', 'title': 'Example Title 2', 'listing': 'F5G6H7I8J', 'price': 200, 'date': '28 June'},
    {'task': 'Example Task 3', 'title': 'Example Title 3', 'listing': 'K9L0M1N2O', 'price': 300, 'date': '29 June'},
]