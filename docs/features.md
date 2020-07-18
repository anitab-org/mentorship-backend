# Features Overview

This backend has many features that allow for members of Mentorship System to establish mentorship relations with each other for a certain period of time.

High level capabilities:

- A member in the system can see other members and choose someone to send a mentorship request to.
- Members can accept, reject mentorship requests and cancel an ongoing mentorship relation.
- Members can wrtie their own profiles and make themselves available to mentor or be mentored.

## Cron jobs

Cron jobs or schedulers are tasks that run from time to time. We have some that aare important for the functionality of the app.

1. Delete unverified users every month. Code can be found [here](/app/schedulers/delete_unverified_users_cron_job.py).

    We have this because we don't want to keep users in our database if they are inactive and have not verified their email.

2. Complete mentorship relations every day. Code can be found [here](/app/schedulers/complete_mentorship_cron_job.py).

    Every day we run a job that completes mentorship relatioons which reached the end date agreed by mentor and mentee.

## Main concepts

These are the main base concepts of the application:

- **User:**  User represents a person that is registered in the application. This has the capability to log in into the Mentorship System. The User can have two roles in the system: mentor or mentee. The user can also be in the app and not assume any of these rules.

- **Mentorship Relation:** A mentorship relation represents a relation between a mentor and a mentee, i.e., two users of the system. It has a time limit, i.e., it can only last for a certain period of time agreed upon by both parties. They can have data shared which are viewed only by them. This data includes tasks, meetings, notes from the agreement between the two users. It also holds information that represents a mentorship agreement between both the mentor and mentee, containing a description of the relation, end date and indication of who assumes the role of mentor and mentee. Learn more about [how it is implemented here](Mentorship-Relation-Documentation).

- **Task:** A task is an assignment that both the mentor and the mentee can create related to a Mentorship Relation. This tasks can be completed, and only then they become achievements of the relation.

_**Note:** This next concept was a part of the initial proposal, not yet implemented._

- **Meeting:** A meeting is an event agreed by mentor and mentee. Any of the users can create it, although they have to agree on it for the meeting to happen. This meeting as a date and time, and optionally a place. The meeting can have some notes attached.

### Mentorship Relation

A **Mentorship Relation** is when two Users, a mentor, and a mentee are matched together to mentor and support each other. This is a 1 to 1 relation, involving just 2 users, during a certain period of time. 

A **Mentorship Relation request** is when a User sends a sort of contract in which the other User has to accept so that a mentorship relation can start. This contract contains notes/description, the definition of who will be the mentor and the mentee and the end date of the relation. Currently, this contract cannot be edited after sent by the User.

#### Conceptual Implementation

Considering two users, _User 1_ and _User 2_. Let's say _User 1_ sends a mentorship request to _User 2_ (next image illustrates this).

<p align="center">
  <img alt="User 1 sends a mentorship relation request to User 2" src="https://user-images.githubusercontent.com/11148726/43965132-68650400-9cb6-11e8-8667-92a181823845.png">
</p>

Looking at the next image, you can consider these 3 stages:
- (1): Before a request is sent
- (2): When the User receives a request
- (3): After a relation starts

---

#### Relation states and stages

<p align="center">
  <img alt="Stages and states of a Mentorship Relation" src="https://user-images.githubusercontent.com/11148726/43964310-73dd99ac-9cb4-11e8-8353-96abadc53ce1.png">
</p>

The next table explains more of the image above.

| State     | Who can trigger this                                                     | How is this triggered                                                                                                                                 | Constraints                                        |
|-----------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| PENDING   | Any User (E.g.: User 1 and User 2)                                       | A User sends/creates a mentorship relation request using the frontend application or backend API                                                      | N/A                                                |
| ACCEPTED  | The User that received the request (E.g.: User 2)                        | The User that received the request can accept this using the frontend application or backend API                                                      | Sets only if the relation is in the PENDING state  |
| REJECTED  | The User that received the request (E.g.: User 2)                        | The User that received the request can reject this using the frontend application or backend API                                                      | Sets only if the relation is in the PENDING state  |
| CANCELLED | Both Users participation in a current relation (E.g.: User 1 and User 2) | Any of the 2 Users participating in the relation can cancel the current relation both on the frontend application or backend API                      | Sets only if the relation is in the ACCEPTED state |
| COMPLETED | A cron job running every day 23h59 (automatically)                       | A cron job in the backend iterates over every mentorship relation, in the ACCEPTED state, and sets this states for relations that passed the end date | Sets only if the relation is in the ACCEPTED state |

**Note:** Even though is not represented in the previous image, the User that sent the mentorship request can delete the request if its state wasn't changed by the receiving User.
