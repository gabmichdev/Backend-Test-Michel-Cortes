# To-Dos of the project.

`x`: Done <br>
`wop`: Work on progress <br>


- [`x`] Allow staff users create menus for a specific date.
- [`x`] Extra: Add different meal times and multiple dishes per menu.
- [`x`] Send a Slack message to all Chilean employees.
- [`x`] Celery setup to excecute periodic tasks in one single process.
- [`x`] Extra: Created a client class to allow for more interactions with Slack.
- [`wop`] Let employees choose preffered meal.
- [`x`] Let employees specify customizations.
- [`wop`] Allow staff to see everyone's requests, but only users to see their own
        requests.
- [`x`] Slack messages contain an URL (with Sites) to today's menu. This has to
        be open for every one to see.

## Known improvements

- Allow creation of individual main, side dishes and desserts instead.
- Filter Chilean users to send each a message, instead of messaging a Slack
  group.
- More extensive testing on some parts of the API.
- Implement Jenkins to create project builds, automated testing pipeline, etc.
- Set some hardcoded values in the docker-compose file environment.
- API documentation, in addition to class, methods and functions docstrings.
- Clutter reduction on the message building part of the project.
- Correct implementation of Celery tasks(creating the actual task in its own
  module instead of importing the function into a task). Been having problems
  with task recognition and excecution.
 