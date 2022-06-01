import csv
import sqlite3

import pandas as pd
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, Review, Title, User

PATH = f'{BASE_DIR}/static/data/'


def csv_to_sqlite(filename, table_name, conn):
    return pd.read_csv(PATH + filename).to_sql(
        table_name, conn, if_exists='append', index=False
    )


class Command(BaseCommand):
    help = 'Загрузка тестовых данных'

    def handle(self, *args, **options):
        for model in [Genre, Category, Comment, Review, Title, User]:
            objs_count = model.objects.count()
            if objs_count:
                model.objects.all().delete()
        self.stdout.write(self.style.WARNING(
            'Deleting old data from database...')
        )
        with open(
            PATH + '/users.csv', mode='r', encoding='utf-8'
        ) as title_data:
            reader = csv.DictReader(title_data)
            User.objects.bulk_create(
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                ) for row in reader
            )

        conn = sqlite3.connect('db.sqlite3')
        csv_to_sqlite('genre.csv', 'reviews_genre', conn)
        csv_to_sqlite('category.csv', 'reviews_category', conn)
        csv_to_sqlite('titles.csv', 'reviews_title', conn)
        csv_to_sqlite('genre_title.csv', 'reviews_title_genre', conn)
        csv_to_sqlite('review.csv', 'reviews_review', conn)
        csv_to_sqlite('comments.csv', 'reviews_comment', conn)
        conn.commit
        conn.close()

        self.stdout.write(self.style.SUCCESS(
            f'''Successfully created:
    {User.objects.count()} users
    {Category.objects.count()} categories
    {Genre.objects.count()} genres
    {Title.objects.count()} titles
    {Review.objects.count()} reviews
    {Comment.objects.count()} comments
            '''
        )
        )
