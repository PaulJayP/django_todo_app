## Todo Task List

Tech task to create a Django based Todo application using postgres running within docker.

### Running

```
Run the application using the command `docker-compose up`

Builds the background services, database, migrations and loads a City/Country dataset into the database.
Used to specify country and city location when adding a task.

Url entrypoint: http://locahost:8080/index
```

### Usage

- Create an account
    - This creates a new user account. This enables the User to create and edit tasks that are owned by that User
- Login
    - Login - This authorizes CRUD on Tasks owned by the User
- Add Task
    - Add a new Task, select location. This returns a temp colour code as well as the temp of the location.
- Edit Task
    - Edit existing Task, select location. Updates the colour code and temp of the location.
- Remove
    - Removes the Task.

#### Testing

Run coverage:

`docker exec -it todo_app_web_1 coverage run --omit='*/venv/*' manage.py test`

Get coverage report

`docker exec -it todo_app_web_1 coverage report`

Run tests

 `docker exec -it todo_app_web_1 python manage.py test --verbosity=2`
