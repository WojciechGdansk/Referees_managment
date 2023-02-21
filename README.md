WebApp to manage and organise football referees tests

Demo on heroku https://manage-referees.herokuapp.com/

WebApp allows to add, view, change, delete questions and organise theoritical exams for football referees. Organizer can browse referees tests results, change league referee belong to, reset password and more.

Referees can solve test created by organizer and see results of tests written in past.

## Demo

https://manage-referees.herokuapp.com/
## Installation

Install packages from requirements.txt -> pip install -r requirements.txt

Write python manage.py loaddata ./fixtures/db.json in terminal to populate database with necessary details(such as leagues and possible answers to choose)

There are four users created with different permissions: 

-admin,

-organizator, username: organiser@op.pl, password: 123, group: Organizator, permissions for most of actions(can change user settings, tests, questions),

-Komisja szkoleniowa, username: szkolenie@op.pl, password: 123, group: Komisja szkoleniowa(can organise tests, check results),

-Sędziowie, username: sedzia@wp.pl, password: 123, group: Sędziowie, can only write tests and check own results

Every new user is automatically added to group Sędziowie.

Test with 30 sample questions is already added, fell free to register(fake email address is fine) and check your football knowledge.
There is 30 minutes to finish test.

Legend:
| | | |  |
| -------- | -------- | -------- | -------- |
| 	G- grać dalej(play-on)	                    | 	J- jeszcze raz (play again)	        | 	R- rzut rożny (corner kick)	     |  	TAK/NIE (Yes/No)	     | 
| 	B- rzut wolny bezpośredni (direct freekick)	| 	S- rzut sędziowski (dropped ball)	| 	Z- zakończenie (terminate game)	 | + - napomnienie (caution)     |
| 	P- rzut wolny pośredni (indirect freekick)	| 	Br- bramka (goal)	                | 	Rb- rzut od bramki (goal kick)	 | ++ - wykluczenie (sent off)   |
| 	K- rzut karny (penalty kick)	            | 	W- wrzut (throw in)             	| 	A, B, C, D, E – wpisz wszystkie poprawne warianty (answers)      | 




## License
This project is Beerware licensed
