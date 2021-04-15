---
id: GSoC-2018-Isabel-Costa
title: GSoC 2018 Isabel Costa
---
## Isabel Costa

I proposed and worked on Mentorship System Backend and Android application. I was mentored by
[Dilushi](https://github.com/Dilu9218), [Murad](https://github.com/m-murad), [Roopal](https://github.com/roopalJazz) and [May](https://github.com/exactlymay) as an admin. 

## Work Hours

| Days      | Hours (WEST = GMT+01) | Meeting                                 | Tool            |
| --------- | --------------------- | --------------------------------------- | --------------- |
| Monday    | 10:00 - 18:00         | Scrum Check-in (5:00 PM)                | Slack           |
| Tuesday   | 10:00 - 18:00         | ------                                  | Slack           |
| Wednesday | 10:00 - 18:00         | Scrum Check-in (5:00 PM)                | Slack           |
| Thursday  | 10:00 - 18:00         | Team Weekly Meeting (4:00 PM)           | Slack, Zoom     |
| Friday    | 10:00 - 18:00         | Scrum Check-in (5:00 PM), GSoC Happy Hour (5:00 PM) | Slack, Zoom     |
| Saturday  | 14:00 - 15:00         | ------                                  | Slack           |
| Sunday    | 14:00 - 15:00         | ------                                  | Slack           |


## Short Bio

I'm an Android Developer and MSc student from Portugal. I'm in the final year of my Master's degree in Telecommunications and Informatics Engineering at Instituto Superior Técnico. I'm mostly interested in Android development, since 2016 when I started working on it. I really like to explore ideas and build projects from an idea into a final product.

## Profile Links
[GSoC Blog](https://medium.com/isabel-costa-gsoc) | [Twitter](https://twitter.com/isabelcmdcosta/) | [Github](https://github.com/isabelcosta) | [LinkedIn](https://www.linkedin.com/in/isabelcmdcosta) | [Medium Blog](https://medium.com/@isabelcmdcosta) | [GSoC 2018 Idea Proposal (partial)](https://docs.google.com/document/d/1TkyLWbVyW9WHEoqFBwpE1GE6vDRf7aoITT6i7tBFKsw/edit?usp=sharing) | GSoC 2018 Finalized Timeline Link?

## Weekly Updates

You can find my updates here: [Weekly Blog post and report status links, Scrum Check-ins, PRs sent](https://docs.google.com/document/d/1OpD7T6Ge0dEEnKBwEuc3Yw2tOUA636m_LXsH9UXB2t8/edit?usp=sharing).

## Final Demo and Report

You can find...
- [My final Demo here](https://www.youtube.com/watch?v=xRZrdR47R-w)!
- [My final Report here](https://gist.github.com/isabelcosta/413e5a58529b7be9cdb57dddc08fec01)

## Weekly Status Report for Week 1

**What have you accomplished this week (list specific items accomplished)?**

- Finished issue #3 - add .gitignore file
- Attended Mentorship Weekly Meeting
- Studied flask materials provided by my mentor and built sample project using Flask-RESTPlus
- Attended GSoC Happy Hour
- Created labels for mentorship-backend repository
- Started working on User Registration API

**What issues or roadblocks have you encountered this week?**

- Problems with PC.
- Thesis reunion and pending work. 
- Lack of experience with backend development with Flask.

**Have they been resolved, and if so, how?**

- The PC is fixed. 
- I’m still a newbie at backend development with flask, but I’m picking up.

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

Thesis reunion will still happen once a week, and I’ll have to work a bit more to prepare for Thesis preparation. To resolve this, I will continue to follow the action items by order and hope to pick up with the schedule in the buffer time defined in the timeline.

**Is further assistance necessary to resolve existing issues?**

One working session with my mentor to get a kick start with the framework.

**What do you plan to accomplish next week?**

Finish this week’s issues, and complete at least 1 issue from the next week

**How does your progress compare to your project schedule?**

I’m late in the schedule, according to the action items proposed on the timeline for 1º week.

**Blog post for Week 1:** [Google Summer of Code | Coding Period | Week 1](https://medium.com/isabel-costa-gsoc/coding-period-week-1-e8f878f46ad9)

-----
## Weekly Status Report for Week 2

**What have you accomplished this week (list specific items accomplished)?**

Submitted PR with these features:
- Completed User actions endpoint
- User authentication to restrict API
- First User is an admin automatically
- Admin user can assign new admins POST /admin/new
- User can update its profile -> PUT /user
- Change Password feature in PUT /user/change_password
- Get all verified users with GET users/verified
- Login with {username, email}+password with POST /auth
- User registration in POST /register endpoint
- List all users with GET /users
- Published and shared Blog post for Week 1
- Attended Project Weekly Meeting
- Shared updates from the project with the community

**What issues or roadblocks have you encountered this week?**

- Thesis reunion and pending work.
- Lack of experience with backend development and testing with Flask.

**Have they been resolved, and if so, how?**

No. Although, I’m feeling more comfortable with developing with flask.

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

- Thesis work will continue until the first week of June.
- I’ve been testing with Postman, but I need to have software tests. I’m still searching for ways to test the REST API, in a modular way (e.g.: test DAO independently of testing database model, ...)

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

- Complete Email verification feature.
- Have some test coverage.
- Start Mentorship Relation feature.

**How does your progress compare to your project schedule?**

Late on Email verification. On time with everything else.

**Blog post for Week 2:** [Google Summer of Code | Coding Period | Week 2](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-2-4019568eabd2)

----
## Weekly Status Report for Week 3

**What have you accomplished this week (list specific items accomplished)?**

- Added initial tests #16
- Fixed Swagger and Postman documentation #20
- Fixed PR template #27
- Had 1:1 with Murad, Dilushi and May
- Created issues for bug fixes and small features #17, #18, #19, #21, #22, #23
- Study ways to implement email verification

**What issues or roadblocks have you encountered this week?**

- Unable to test API resources, probably because of app structure
- Squashing commits
- Thesis

**Have they been resolved, and if so, how?**

- For tests, not yet.
- For squashing commits, had help from Dilushi.
- Regarding Thesis, not yet.

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

- I’m still studying about it tests
- Thesis work will end next week

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

- Submit PR for email verification API
- Submit PR for mentorship relation API
- Setup support for environment variables

**How does your progress compare to your project schedule?**

Late on email verification and mentorship relation

**Blog post for Week :** [Google Summer of Code | Coding Period | Week 3](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-3-349e08f7d998)

----
## Weekly Status Report for Week 4

**What have you accomplished this week (list specific items accomplished)?**

- Created issues reported by Murad (#33, #34, #35)
- Solved above issues
- Created tests for app configurations (#37) 
- Attended project weekly
- Reviewed Mentorship Relation feature in project weekly meeting
- Created issue for sending the expiry date on Login response #39

**What issues or roadblocks have you encountered this week?**

1. Thesis final presentation
2. API Resources Testing

**Have they been resolved, and if so, how?**

1. Yes, it is presented!
2. No

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

1. N/A
2. I’m still studying about it tests, planning to have a working session with Murad

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

- Fill 1st Evaluations
- Complete Mentorship Relation feature
- Have tests for API resources
- Demo Mentorship System Backend in Community Open Session
- [stretch goal] Do email verification

**How does your progress compare to your project schedule?**

Late on email verification.

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 4](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-4-52eb3bb0bf41)

----
## Weekly Status Report for Week 5

**What have you accomplished this week (list specific items accomplished)?**

1. Had 1:1 meeting with May
2. Started working on mentorship send/listing request feature
3. Had 1:1 meeting with Dilushi
4. Attended Project weekly and clarified doubts about the database model and main features of the system
5. Submitted PR #47 for sending a request (issue #10) and getting all mentorship requests (issue #46)
6. Created new issues from bugs and feature clarification (#48, #49 and #50)

**What issues or roadblocks have you encountered this week?**

1. Understand Mentorship System complex features and database model

**Have they been resolved, and if so, how?**

1. Yes, this was clarified in the project weekly. To have a minimum viable product in the end of this program, we simplified some features

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

No

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

1. Complete Mentorship Relation related features (send, accept, reject, cancel requests)
2. Setup issues for the second phase of the coding period
3. Continue working on email verification feature

**How does your progress compare to your project schedule?**

Late on mentorship feature, email verification

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 5](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-5-740cda442109)

---

## Weekly Status Report for Week 6

**What have you accomplished this week (list specific items accomplished)?**

1. Submitted PR #41 to add support for using environment variables
2. Submitted PR #53 for email verification - issues #7, #5 (need to fix according to the weekly meeting)
3. Submitted PR #54 for creating the API to remove an Admin user - issue #17 (fixed logic according to the meeting)
4. Created issue #52 to update restricted APIs to verify is user has email verified
5. Organized issues on Zenhub according to dependant PRs and Issues
6. Attended project weekly meeting, clarified some doubts

**What issues or roadblocks have you encountered this week?**

Thesis document fixes

**Have they been resolved, and if so, how?**

Yes, they’re done

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

No

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

1. Have completed accept/reject/cancel/complete 
2. Deploy Backend
3. Share the deployed backend update with the community and ask for feedback and testing
4. Refactor app to be able to test the API
5. [stretch goal dependent on the stability of backend] Start working on Android Application

**How does your progress compare to your project schedule?**

I’m on time with the backend

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 6](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-6-64e8660530fe)

---

## Weekly Status Report for Week 7

**What have you accomplished this week (list specific items accomplished)?**

1. Had a 1:1 with Murad and another 1:1 with Dilushi
2. Submitted PR #57 for applying the Application Factory pattern (important for testing the REST API services) issue #55  (merged)
3. Submitted PR #58 for accepting mentorship relation API (merged)
4. Submitted PR #62 for reject a mentorship request API (merged)
5. Submitted PR #61 for cancel a mentorship request API (merged)
6. Submitted PR #59 to update PR template, to update requirements.txt (merged)
7. Finished email verification feature (PR #53)
8. Submitted PR #64 for flask-jwt-extended integration
9. Wrote blog post about mentorship system (motivation & about)
10. Started working on a cron job to complete a mentorship relation
11. Started working on exporting automatically generated postman.json and swagger.json
12. Created issues to use flask-jwt-extended instead of flask-jwt
13. Attended project weekly (cleared features logic doubts)
14. Created issues #66 to eventually add an extra field to explain reasoning for mentorship cancellation
15. Created issue #65 for a delete mentorship request API

**What issues or roadblocks have you encountered this week?**

1. Application factory pattern PR merge

**Have they been resolved, and if so, how?**

Yes, it has been merged and I can now do API testing :D

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

No :D

**Is further assistance necessary to resolve existing issues?**

No!

**What do you plan to accomplish next week?**

TBD

**How does your progress compare to your project schedule?**

More productive than other weeks. Still on backend

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 7](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-7-2e8e4f1b206d)

-----

## Weekly Status Report for Week 8

**What have you accomplished this week (list specific items accomplished)?**

1. Submitted PR #73 for API to delete a mentorship request
2. Submitted PR #74 for Get all mentorship requests API
3. Submitted PR #75 to restrict GET /users API to authenticated users
4. Submitted PR #79 with cron job to complete mentorship relation
5. Attended Project Weekly
6. Made Demo and presented Mentorship Systems backend on Community Open Session
7. Got [Mentorship System by Systers](https://medium.com/systers-opensource/mentorship-system-by-systers-52dbe1275d9f) blog post published on Systers Open Source Medium publication
8. Worked with Murad to solve server deployment issues
9. Defined minimum features for the minimum functional product

**What issues or roadblocks have you encountered this week?**

1. Cron job to complete mentorship relations
2. Server deployed was failing to receive authorization header

**Have they been resolved, and if so, how?**

1. Yes, its done, I tested interval and cron schedulers until I saw this working
2. Yas! I worked with Murad to solve this issue

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

No

**Is further assistance necessary to resolve existing issues?**

No

**What do you plan to accomplish next week?**

1. Have new wireframe for the minimum functional product
2. Start working on the android app
3. Improve overall Github documentation to guide potential contributors
4. Decide on issues for newcomers, quality assurance (e.g.: manual and coding testing) with Dilushi

**How does your progress compare to your project schedule?**

On time regarding finishing the backend and heading towards the android app

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 8](https://medium.com/isabel-costa-gsoc/google-summer-code-coding-period-week-8-c10271254a67)

------

## Weekly Status Report for Week 9

**What have you accomplished this week (list specific items accomplished)?**

1. Created Quality Assurance Google Docs to guide contributors to test the backend
2. Invited newcomers to test the backend and provided documentation for that
3. Defined minimum features and timeline for phase 3
4. Had 1:1s with May, Murad and Dilushi
5. Created the high fidelity UI prototype (created issue #1 for this on systers/mentorship-android repo)
6. Studied Material Design for the wireframe
7. Fixed bug from issue #84, PR #85
8. Looked into Android architecture design patterns
9. Created with Dilushi the first issue #86 regarding Quality Assurance for the backend
10. Attended project weekly meeting
11. Created issue and discussed Tasks feature in project meeting
12. Reserved time of the week (available on Google Calendar) and became available to answer any questions from newcomers (AMA - Ask Me Anything sessions)

**What issues or roadblocks have you encountered this week?**

No

**Have they been resolved, and if so, how?**

N/A

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

N/A

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

1. Improve UI according to feedback given by the community
2. Study about Clean architecture
3. Finish Tasks feature
4. Attend Project Weekly meeting
5. Start User arc feature in Android application
6. Host more AMA sessions for newcomers
7. Create issues for newcomers (stretch goal)

**How does your progress compare to your project schedule?**

On time to do the Android app!

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 9](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-9-4affc5a70580)

-------

## Weekly Status Report for Week 10

**What have you accomplished this week (list specific items accomplished)?**

- Hosted more AMA sessions
- Had first 1:1 with Roopal, my new mentor and a 1:1 with Murad
- Studied Android Architectures
- Worked on Tasks feature
- Fixed merge conflict of PRs #90 and #85 which are now merged
- Created issue #94 and submitted PR #95 to solve user registration data validation
- Submitted PR #89 imports database URI from environment variables (persistence to DB)
- Submitted PR #90 that adds organization field to User (occupation was already there)
- Reviewed PR #105 regarding change password request data validation 

**What issues or roadblocks have you encountered this week?**

Learning Clean architecture

**Have they been resolved, and if so, how?**

Yes, I moved to learn another Architecture, MVVM, which seems less complex for a project being built from scratch. Clean architecture would add unnecessary  complexity for this app.

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

No

**Is further assistance necessary to resolve existing issues?**

No

**What do you plan to accomplish next week?**

- Have User arc completed
- Start Mentorship Relation arc
- Fix more bugs found from the Backend
- Host more AMA sessions
- Present a Demo of Phase I & II

**How does your progress compare to your project schedule?**

Late on the Mobile app development, should have started the User arc already

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 10](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-10-191813534051)

-----

## Weekly Status Report for Week 11

**What have you accomplished this week (list specific items accomplished)?**

1. Had 1:1s: 1 w/ May, 3 w/ Murad, 1 w/ Dilushi
2. Hosted AMA session for newcomers
3 Created issues on systers/mentorship-backend -> #115, #116
4. Created issues on systers/mentorship-android -> #2, #3, #4, #5, #6, #7, #8, #9, #11
5. Created “How to Contribute” page on Backend repository Wiki and created Wiki on systers/mentorship-android
6. Reported bug #114, #120 and docs issue #120  on #sysbot
7. Attended Project Weekly
8. Exported UI screens from JustInMind UI prototype and saved them on GSoC18 folder
9. Presented for Demo Phase I & II
10. Shared in the community the Tasks feature logic decisions and potential scalability issue (which I researched a solution for)
11. Add some markdown tables with some test cases on Quality Assurance issues
12. Share the UI feedback Google Docs document for Q&A
13. Updated the UI prototype in JustInMind tool and update the Feedback Google Docs
14. Submitted PR #107 to solve issue #97 (already fixed merge conflicts)
15. Had 1:1 Sammy about GitHub workflow with Sysbot and its commands

**What issues or roadblocks have you encountered this week?**

1. Understanding RxJava, Android Architecture components, and best practises
2. Tasks feature implementation
3. Testing on Android

**Have they been resolved, and if so, how?**

1. Mildly
2. No
3. No

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

1. Sort of, since I’m still learning this
2. Yes it still exists, thinking of doing a meeting to talk about this
3. Yes, I’ll search about this, and check how it’s being done on Systers Android apps

**Is further assistance necessary to resolve existing issues?**

1. No, because I already got this week from Murad
2. Meet with mentors about this
3. Will research about this

**What do you plan to accomplish next week?**

1. Complete User arc and Mentorship and start Tasks arc
2. Fix some bugs of Backend
3. Start Tasks arc
4. Manage more issues
5. Attend Project Weekly
5. Host more AMA sessions

**How does your progress compare to your project schedule?**

Late on the Android application

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 11](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-11-799f11918c62)

-----

## Weekly Status Report for Week 12

**What have you accomplished this week (list specific items accomplished)?**

1. Had 1:1 with Murad (discussed best practices for Android)
2. Created .svg file of Current Relation icon
3. Added Travis CI support to Android repository
4. Submit PR #17 with my initial code (register, login, bottom nav) 
5. List Item UI of All Members list with ConstraintLayout (on my fork only)
6. My Profile Screen UI with ConstraintLayout (on my fork only)
7. Hosted AMA sessions
8. Attended project weekly
9. Created issues important for Android application #121 and #120 on Backend
10. Solved issue #121 from backend (waiting on issue to be approved)

**What issues or roadblocks have you encountered this week?**

1. Tasks scalability issue still has to be solved
2. First PR took some time to be merged since is was the base for the authenticated fragments and Codacy alerted about some issues with the code and travis CI had to be set

**Have they been resolved, and if so, how?**

1. No
2. Yes, it was merged, Codacy warnings were fixed, and travis CI integrated

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

1. Yes
2. No

**Is further assistance necessary to resolve existing issues?**

1. Yes, need to have a discussion with mentors

**What do you plan to accomplish next week?**

1. Complete User and MentorshipRelation arc
2. Decide on Tasks scalability issue
3. Off-board the project

**How does your progress compare to your project schedule?**

Late on the Android application

**Blog post for Week:** [Google Summer of Code | Coding Period | Week 12](https://medium.com/isabel-costa-gsoc/google-summer-of-code-coding-period-week-12-e14533ce7159)

----

## Weekly Status Report for Week 13 [Optional]

**What have you accomplished this week (list specific items accomplished)?**

1. Submitted PR #123 for restructuring MentorshipRelation response to include Name (backend)
2. Submit PR for listing Members Screen and Check others’ profiles (android)
3. Had 1:1 with May
4. Had 2 1:1s with Murad
5. [Backend] Solve issue #124 on backend and sent PR #126
6. Attended Weekly Meeting
7. Removed “Program: GSoC” labels and added “Status: Available” to issues not completed during the program and ready to be worked by any contributor
8. Created Wiki page with references to UI Design on systers/mentorship-android repo
9. Created Wiki pages to explain a mentorship relation stages and states on systers/mentorship-android and systers/mentorship-backend repo
11. [Android] Submit PR for Requests Screen
12. Presented Final Demo
13. Finished GSoC Final Report
14. [Backend] Submitted Tasks feature
15. Submitted Final Evaluations
16. Submitted PR for README
17. Started improving GitHub Wiki documentation

**What issues or roadblocks have you encountered this week?**

1. Tasks scalability issue
2. Final Demo

**Have they been resolved, and if so, how?**

1. Yes its done!
2. Yes, its done!

**Do any of the issues or roadblocks still exist and what steps have been taken to resolve them?**

1. No
2. No

**Is further assistance necessary to resolve existing issues?**

N/A

**What do you plan to accomplish next week?**

Help newcomers start working on issues and make the project welcome to everyone

**How does your progress compare to your project schedule?**

Ready to be worked on and welcome contributors!

**Final Blog post:** [Google Summer of Code final remarks](https://medium.com/isabel-costa-gsoc/gsoc-with-systers-community-closure-43d8e135c153)
