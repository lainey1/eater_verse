from app.models import db, Restaurant, environment, SCHEMA
from sqlalchemy.sql import text


# Adds demo restaurants
def seed_restaurants():
    restaurant1 = Restaurant(
        owner_id=1,
        address='123 Burger Lane',
        city='New York',
        state='NY',
        country='USA',
        phone_number='212-555-6789',
        email='info@mainstcafe.com',
        website='https://www.burgerhaven.com',
        hours={
            "Monday": ["9:00 AM", "9:00 PM"],
            "Tuesday": ["9:00 AM", "9:00 PM"],
            "Wednesday": ["9:00 AM", "9:00 PM"],
            "Thursday": ["9:00 AM", "9:00 PM"],
            "Friday": ["9:00 AM", "10:00 PM"],
            "Saturday": ["10:00 AM", "10:00 PM"],
            "Sunday": ["10:00 AM", "8:00 PM"]
        },
        name='Burger Haven',
        cuisine='American',
        price_point=2,
        description='Juicy gourmet burgers and hand-cut fries.'
    )
    restaurant2 = Restaurant(
        owner_id=2,
        name='Chez Paris',
        address='456 Rue de Paris',
        city='San Francisco',
        state='CA',
        country='USA',
        phone_number='415-555-1234',
        email='bonjour@chezparis.com',
        website='https://www.chezparis.com',
        hours={
            "Monday": ["8:00 AM", "10:00 PM"],
            "Tuesday": ["8:00 AM", "10:00 PM"],
            "Wednesday": ["8:00 AM", "10:00 PM"],
            "Thursday": ["8:00 AM", "11:00 PM"],
            "Friday": ["8:00 AM", "12:00 AM"],
            "Saturday": ["9:00 AM", "12:00 AM"],
            "Sunday": ["9:00 AM", "9:00 PM"]
        },
        cuisine='French',
        price_point=4,
        description='Classic French dishes with a modern twist.'
    )
    restaurant3 = Restaurant(
        owner_id=3,
        name='Trattoria Italiana',
        address='789 Pasta Place',
        city='Chicago',
        state='IL',
        country='USA',
        phone_number='312-555-2468',
        email='info@trattoriaitaliana.com',
        website='https://www.trattoriaitaliana.com',
        hours={
            "Monday": ["11:00 AM", "9:00 PM"],
            "Tuesday": ["11:00 AM", "9:00 PM"],
            "Wednesday": ["11:00 AM", "9:00 PM"],
            "Thursday": ["11:00 AM", "10:00 PM"],
            "Friday": ["11:00 AM", "10:00 PM"],
            "Saturday": ["12:00 PM", "10:00 PM"],
            "Sunday": ["12:00 PM", "9:00 PM"]
        },
        cuisine='Italian',
        price_point=3,
        description='Authentic Italian pasta and wood-fired pizzas.'
    )
    restaurant4 = Restaurant(
        owner_id=4,
        name='Sushi Station',
        address='789 Sushi Street',
        city='Los Angeles',
        state='CA',
        country='USA',
        phone_number='213-555-9876',
        email='hello@sushistation.com',
        website='https://www.sushistation.co',
        hours={
            "Monday": ["11:00 AM", "9:00 PM"],
            "Tuesday": ["11:00 AM", "9:00 PM"],
            "Wednesday": ["11:00 AM", "9:00 PM"],
            "Thursday": ["11:00 AM", "10:00 PM"],
            "Friday": ["11:00 AM", "10:00 PM"],
            "Saturday": ["12:00 PM", "10:00 PM"],
            "Sunday": ["12:00 PM", "9:00 PM"]
        },
        cuisine='Japanese',
        price_point=3,
        description='Fresh sushi and sashimi served daily.'
    )

    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.add(restaurant3)
    db.session.add(restaurant4)
    db.session.commit()



# Uses a raw SQL query to TRUNCATE or DELETE the restaurants table.
# SQLAlchemy doesn't have a built-in function to do this.
# With Postgres in production, TRUNCATE removes all the data from the table,
# and RESET IDENTITY resets the auto-incrementing primary key, CASCADE deletes
# any dependent entities. With SQLite in development, use DELETE to remove
# all data and it will reset the primary keys for you as well.
def undo_restaurants():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.restaurants RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM restaurants"))

    db.session.commit()
