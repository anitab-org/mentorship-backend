---
id: Technical-Decisions
title: Technical Decisions
---
**Table of Contents**
- [Why Development Backend is hosted on Heroku?](#march-2020---why-development-backend-is-hosted-on-heroku)
- [Why use AWS?](#august-2018---why-use-aws)
- [Tasks data model implementation](#july-2018---tasks-data-model-implementation)
- [Why use Flask framework?](#may-2018---why-use-flask-framework)
- [Why use Flask-RESTPlus?](#may-2018---why-use-flask-restplus)
- [Why use Flask-JWT-Extended instead of just Flask-JWT?](#may-2018---why-use-flask-jwt-extended-instead-of-just-flask-jwt)

**Outstanding decisions to review and discuss:**
- Hard delete of entities from Mentorship System, vs masking information or only removing sensitive data ([#delete-entities topic on Zulip](https://anitab-org.zulipchat.com/#narrow/stream/222534-mentorship-system/topic/deleting-entities))
- Mentorship Relation Tasks data model implemented other than JSON custom object ([#task implementation topic on Zulip](https://anitab-org.zulipchat.com/#narrow/stream/222534-mentorship-system/topic/Tasks.20implementation))
- API versioning ([Issue #481](https://github.com/anitab-org/mentorship-backend/issues/481))

## XX/XX/XX - Topic

N/A

## March 2020 - Why Development Backend is hosted on Heroku?

We were using AWS, but the Backend stopped working (500 error) after one specific deploy, which we could not investigate due to not having appropriate access for it (AnitaB.org IT team has the credentials). So [Isabel](https://github.com/isabelcosta) decided to deploy it on Heroku, so we could continue having a Swagger UI endpoint for the REST API that people could access it for testing purposes. So until we have proper access to AWS, we are using Heroku. 

## August 2018 - Why use AWS?

AWS is being used since other previous projects were using AWS as well, such as [systers/portal](https://github.com/anitab-org/portal). Although other projects in the community use [Heroku](https://www.heroku.com/).

## July 2018 - Tasks data model implementation

Due to concerns regarding a problem of scalability with saving Tasks into the relational database as an entity, we identified the potential issue.

**Problem:** Tasks of a mentorship relation are easy to grow in number. Let's imagine at a certain time in the future we have 500 relations and each of them having 50 tasks (50 per each relation). That’s in total 500*50 tasks scattered through the Tasks table, and to get tasks from a specific current relation, a cursor will have to iterate over the whole table. This causes a scalability issue.

**Potential solution:** We agreed that we would search a solution for this besides saving as a string.

After some research about this Isabel found that SQLAlchemy allows to use of JSON objects, and MySQL since version 5.7 allows this to happen:
- http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.JSON
- https://stackoverflow.com/a/15367769/6094482

Here's [Task Scalability Google Docs](https://docs.google.com/document/d/1Bm0SAPSKjxZNRkDsvklPdtbHxLXsHQpsPLz4m18nzC4/edit?usp=sharing) where Isabel tried to document a discussion at the time with mentors. We decided to go with JSON format to store the tasks list, but we agreed to review this model later after GSoC.

Some ideas were thrown since then: Using Postgres directly instead of the SQLAlchemy abstraction, using indexing, creating the Tasks model anyways?!

By the way, this was implemented on [PR #128](https://github.com/anitab-org/mentorship-backend/pull/128).

## May 2018 - Why use Flask framework?

The GSoC student did not have experience with backend and the mentors had experience with python. One of the mentors suggested Flask framework since it was fairly simple to pick up and quickly bootstrap a REST API application.

## May 2018 - Why use Flask-RESTPlus?

Flask-RESTPlus is the core of this backend. The REST API is built using this flask extension. The main advantage is that it supports Swagger Documentation. With this tool, we can develop the API while using annotations that help to generate the Swagger UI.

You can know more about how to use Swagger in [this page](Using-Backend-Swagger-UI).

## May 2018 - Why use Flask-JWT-Extended instead of just Flask-JWT?

[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/) provides great support for [JSON Web Tokens (JWT)](https://jwt.io/) based Authentication. It provides a lot of flexibility

You can learn more about how [User Authentication](User-Authentication) is done in this project.

Initially, we started using [Flask-JWT](https://pythonhosted.org/Flask-JWT/), but as the development progressed we started having challenges to solve that required a more flexible library. One of the issues that made us change to _Flask-jwt-extended_ was the need for extra verifications while login in a User into the system, specifically verifying if the user had the email verified. After looking into _flask-jwt_ source code and docs to see if this could be done easily the GSoC student concluded that it would require extra work by having to override some functions, as done before, and that this would overcomplicate code. Ultimately, it was agreed with the mentors to use _flask-jwt-extended_ that provided more flexibility to implement the Login API. The official documentation of _flask-jwt-extended_ shows an [example of the basic usage](http://flask-jwt-extended.readthedocs.io/en/latest/basic_usage.html) of the extension, where it shows the flexibility to verify extra fields and properties and provide custom error messages.