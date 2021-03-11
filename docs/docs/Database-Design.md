---
id: Database-Design
title: Database Design
---
This page aims to explain Database design of the app and some implementation decisions.

## Main data models

Learn more about the core concepts - User, Mentorship Relation and Tasks - in [Main Base Concepts Page](Main-Base-Concepts).

## Why Tasks is currently wrapped in TaskList JSON Object

Back in Google Summer of Code 2018, mentors and the student decided to implement Tasks as a JSON Object because of potential scalability issues.

Here's a discussion thread about this approach:
- [Discussion starter message on Systers Open Source Slack](https://systers-opensource.slack.com/archives/C0S15BFNX/p1532623507000096/), here is the continuation [thread](https://systers-opensource.slack.com/archives/C0S15BFNX/p1532624183000470/).
- [Task Scalability issue Google Docs (not so updated)](https://docs.google.com/document/d/1Bm0SAPSKjxZNRkDsvklPdtbHxLXsHQpsPLz4m18nzC4/) (the above thread may have more useful info).