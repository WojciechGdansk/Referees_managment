WebApp to manage referees tests

1. Install packages from requirements.txt -> pip install -r requirements.txt
2. Write python manage.py loaddata ./fixtures/db.json in terminal to populate database with necessary details(such as
   leagues and possible answers to choose)
3. There are four users created with different permissions:
   -admin
   -organizator, username: organiser@op.pl, password: 123, group: Organizator, permissions for most of actions(can
   change user settings, tests, questions)
   -Komisja szkoleniowa, username: szkolenie@op.pl, password: 123, group: Komisja szkoleniowa(can organise tests, check
   results)
   -Sędziowie, username: sedzia@wp.pl, password: 123, group: Sędziowie, can only write tests and check own results
4. Every new user is automatically added to group Sędziowie
5. Few sample questions are added in database