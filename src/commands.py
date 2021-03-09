from flask import Blueprint, current_app

from src import db

db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("DB Created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from src.models.User import User
    from src import bcrypt
    from faker import Faker
    import random

    faker = Faker()
    users = []
    TEST_PASSWORD = current_app.config["TEST_PASSWORD"]

    if not TEST_PASSWORD:
        raise ValueError('TEST_PASSWORD not provided.')

    for i in range(5):
        # Add users
        user = User()
        user.email = f"test{i}@test.com"
        user.bio = faker.paragraph(nb_sentences=3)
        user.username = f"test{i}"
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.password = bcrypt.generate_password_hash(f"{TEST_PASSWORD}").decode("utf-8")
        db.session.add(user)

    db.session.commit()


    print("Users Added")
    print("Tables seeded")
