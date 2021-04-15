---
id: Mentorship-Relation-Documentation
title: Mentorship Relation Documentation
---
A **Mentorship Relation** is when two Users, a mentor, and a mentee are matched together to mentor and support each other. This is a 1 to 1 relation, involving just 2 users, during a certain period of time. 

A **Mentorship Relation request** is when a User sends a sort of contract in which the other User has to accept so that a mentorship relation can start. This contract contains notes/description, the definition of who will be the mentor and the mentee and the end date of the relation. Currently, this contract cannot be edited after sent by the User.

## Conceptual Implementation

Considering two users, _User 1_ and _User 2_. Let's say _User 1_ sends a mentorship request to _User 2_ (next image illustrates this).

<p align="center">
  <img alt="User 1 sends a mentorship relation request to User 2" src="https://user-images.githubusercontent.com/11148726/43965132-68650400-9cb6-11e8-8667-92a181823845.png" />
</p>

Looking at the next image, you can consider these 3 stages:
- (1): Before a request is sent
- (2): When the User receives a request
- (3): After a relation starts

---

### Relation states and stages

<p align="center">
  <img alt="Stages and states of a Mentorship Relation" src="https://user-images.githubusercontent.com/11148726/43964310-73dd99ac-9cb4-11e8-8353-96abadc53ce1.png" />
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

