# django_test

how to run:
1. make sure you have docker install and running.
2. clone the repo.
3. open terminal and navigate to the repo clone root folder.
4. run the following commands in the terminal:
 I. docker-compose run web python manage.py migrate.
 II. docker-compose up
5. to shut down the project,  press ctrl+c

note: in real world, the secrets and .env file would not be saved in the repo.
