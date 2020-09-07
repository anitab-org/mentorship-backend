---
id: Main-Base-Concepts
title: Main Base Concepts
---
These are the main base concepts of the application:

- **User:**  User represents a person that is registered in the application. This has the capability to log in into the Mentorship System. The User can have two roles in the system: mentor or mentee. The user can also be in the app and not assume any of these rules.

- **Mentorship Relation:** A mentorship relation represents a relation between a mentor and a mentee, i.e., two users of the system. It has a time limit, i.e., it can only last for a certain period of time agreed upon by both parties. They can have data shared which are viewed only by them. This data includes tasks, meetings, notes from the agreement between the two users. It also holds information that represents a mentorship agreement between both the mentor and mentee, containing a description of the relation, end date and indication of who assumes the role of mentor and mentee. Learn more about [how it is implemented here](Mentorship-Relation-Documentation).

- **Task:** A task is an assignment that both the mentor and the mentee can create related to a Mentorship Relation. This tasks can be completed, and only then they become achievements of the relation.

_**Note:** This next concept was a part of the initial proposal, not yet implemented._

- **Meeting:** A meeting is an event agreed by mentor and mentee. Any of the users can create it, although they have to agree on it for the meeting to happen. This meeting as a date and time, and optionally a place. The meeting can have some notes attached.