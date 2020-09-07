---
id: Code-Organization
title: Code Organization
---
This page explains how the project is structured.

## Basic Architecture

<p align="center">
  <img alt="basic architecture" src="https://user-images.githubusercontent.com/11148726/44174311-ac5eaa80-a0da-11e8-92bb-ca2fe7c26f60.png" />
</p>

**Main Components:**
- **Data Model:** This contains all database models, which are implemented using SQLAlchemy Model abstraction, e.g.: UserModel, MentorshipRelationModel.
- **Data Access Object (DAO):** These classes contain functions used by the API resources and use Database Models.
- **API Resources:** This is responsible for the REST API available form the deployed server. These resources define the namespaces, i.e., resources HTTP methods. It's also responsible for Swagger documentation.

### Root project structure

| Folders and files | Description                                                                                             |
|-------------------|---------------------------------------------------------------------------------------------------------|
| .github           | Contains files related to GitHub (e.g.: pull request and issue templates, contributing guidelines, ...) |
| app               | Contains most of the development code                                                                   |
| docs              | Contains non-production code (e.g.: Swagger and Postman template to test API)                           |
| templates         | Contains html templates used by the app (e.g.: verification email template)                             |
| tests             | Contains all unit tests                                                                                 |
| config.py         | Has the different set of configurations the app can run with                                            |
| run.py            | Main entry point of the app                                                                             |
| requirements.txt  | Describes all dependencies of the app                                                                   |
