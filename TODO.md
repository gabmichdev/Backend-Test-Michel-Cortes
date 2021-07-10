# To-Dos of the project.

`x`: Done <br>
`wop`: Work on progress <br>


- [`x`] Allow staff users create menus for a specific date.
- [`x`] Extra: Add different meal times and multiple dishes per menu.
- [`x`] Send a Slack message to all Chilean employees.
- [`x`] Celery setup to excecute periodic tasks in one single process.
- [`x`] Extra: Created a client class to allow for more interactions with Slack.
- [`x`] Let employees choose preffered meal.
- [`x`] Let employees specify customizations.
- [`x`] Let employees specify customizations before 11 AM.
- [`x`] Allow staff to see everyone's requests, but only users to see their own
        requests.
- [`x`] Slack messages contain an URL (with Sites) to today's menu. This has to
        be open for every one to see.

## Known improvements

- Setup a series of internal debugging tools that automatically turn off based
  on an environment variable.
- Make a robust implementation to deal with timezone issues. App is using UTC
  as the timezone, which would make people eat breakfast quite early.
- Implement translation module correctly to translate errors and messages.
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

## Known errors
- In the MenuSelection serializer, using the MenuSerializer to populate the
  menus gives null menu_id error when creating MenuSelections. Must leave it as
  and receive as response the menu_id only.
- When creating custom validation error to accomodate for the MenuSelection
  creation conditions, sending `rest_framework.status.HTTP_400_BAD_REQUEST` 
  returns a response such as
  ```json
  {
    "detail": "No puedes seleccionar un menu de otro dia o despues de las 11"
  }
  ```
  ...therefore the assertion gives the following error:
  ```python
  self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  AttributeError: 'str' object has no attribute 'status_code'
  ```
  However, if the APIException is raised with any other status code such as 422
  no such error occurs: 
  ```python
  self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  AssertionError: 422 != 400
  ```
  *Update* Fixed error, another assertion (after this one) was causing this one
  to give that error, removed said assertion since it was not correct either
  way.
 