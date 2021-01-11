# Creating Meetings Between Members

There might be a need to create meetings between two members, possibly between a mentor and mentee . A meeting may be set up by the mentor for the mentee and both go to the meeting spot at the scheduled time. The meeting spot may be a physical location or a video conference link.

To develop a MVP for this feature, the following few conditions need to be pondered about:

1. **Market Situation**:  Such meetings and their scheduling exist in the present market in many organisations. We can take ideas from how they schedule their meetings (say using Google Meet and Google Calendar), the interface of creating these meetings, etc. and develop a similar interface for our organisation.
2. **User Journey Creation**: We need to define the experience or journey that a user will go through while using this feature. A possible option can be that a mentor creates a new meeting, adds a mentee (or a group of mentees) to the meeting's list of attendees, schedules a date and time for the meeting, and obtains the link for the meeting and shares it with the mentees. The mentees then join the meet link at the scheduled time.
3. **Deciding the Database Models, Associated Methods and Requests**: Once the essential features for the meetings have been decided, a database model to represent these meetings can be outlined and associated API methods and requests can be made to create, update and get data about these meetings.

A simple and minimalistic MVP for implementing the Meeting feature is described below.


## Database Models
```
model Meeting:
A model to represent a meeting in the database. 
Class attributes:
	- integer object : meeting_id
	- attendee object : host (or the meeting creator)
	- list object : invitees (list of users invited to the meeting)
	- list object : attendees (list of final attendees who agree to come to the meeting)
	- datetime object : start_date_and_time
	- datetime object : end_date_and_time
	- datetime object : duration
	- string object : meeting_link


model Attendee:
A model to represent an attendee object associated with a user (mentee/mentor) 
Class attributes:
	- integer object : user_id (user id of the user associated)
	- integer object : upcoming_scheduled_meeting (meeting id of the meeting that the attendee is currently having an appointment in)'
	- list object : scheduled_meetings (list of all meetings that the attendee is going to attend)
		
```

## Resources
Helper classes and methods to interact with the models
```
class CreateAttendee:
	
	method post():
		# A new attendee object is created and a ONE-TO-ONE relationship is established 
		  with the request user and the attendee object
		
class GetAttendee:

	method get(user_id):
		# Attendee object associated with the user with id
		 "user_id" is fetched from the database and returned. 
		  If the attendee object doesnt exist then an exception is raised.
		
class CreateMeeting:

	method post():
		# A JSON object containing request data about date and time of meeting, list of invitees is extracted. 
		Check are done to check for the validity of the invitees. If there is any discrepancy, an exception is raised. 
		Else, a new meeting object is created with host as the request user. 
		A follow-up method to send invite links to all the invitees is then executed. 

class UpdateMeeting:
		method put( meeting_id ):
				# The meeting with the meeting id = "meeting_id" is extracted from the database. 
				If the meeting doesn't exist, an exception is raised. 
				Else, the meeting details are updated with data extracted from request data. 
				Follow-up methods are correspondingly executed to send updated invite links.

class GetAllMyInvites:
	method get():
		# Fetches and returns a list all the meetings that the attendee has been invited to.
		
class AcceptMeetingInvite:
	method post(meeting_id):
		# The meeting with the meeting id = "meeting_id" is extracted from the database. 
		  If the meeting doesn't exist, an exception is raised.
		  Else, the meeting is added to the attendee's list of meetings. 
		  A follow-up method is also executed to add the attendee to the meeting's list of attendees. 

class AcceptMeetingInvite:
	method post(meeting_id):
		# The meeting with the meeting id = "meeting_id" is extracted from the database. 
		  If the meeting doesn't exist, an exception is raised.
		  Else, the meeting is added to the attendee's list of meetings. 
		  A follow-up method is also executed to add the attendee to the meeting's list of attendees.
		  
class GetAllMyMeetings:
	method get():
		# Fetches and returns a list all the meetings that the attendee has accepted to attend.

class GetMeeting:
	method get(meeting_id):
		# Fetches the meeting object with meeting_id = "meeting_id" and checks if the request user has been invited to the meeting and the user is attending the meeting. 
		If the user is not attending the meeting an exception is raised, otherwise the meeting object is returned to the user. 
		If no such meeting object exists, an exception is raised.

```



## Integration with Google Calendar

Google Meets and Google Calendar give a really good inspiration as to how this feature can be implemented. When a meeting is set up in Google Meet, invite links are emailed to attendees. There are buttons on those invite links to respond whether the attendee would be coming to the meet or not. 

We can have a similar user journey in our feature. Once a meeting object is created, invite links can be accessed by the invitees via the methods and resources mentioned in the previous section. Responding a YES to the invite on the UI will add the user to the list of the meeting's attendees. A follow-up method can be implemented to consequently add an event to the Google Calendar associated with the attendee's email using the meeting's details. This can be made possible by using the Calendar API to add and update events. An additional feature could be that if the meeting link is a Google Meet link, then the meeting can be even more easily added to the user's calendar then.

## Future Expansion

The Meeting and Attendee Model and Interface illustrated above can be also used to further add class attributes to the models and adding more methods to the interface. The interface helps in easy expansion according to needs of the time, and considers several OOP practices like encapsulation and abstraction. A suitable DAO can be implemented to interact with the database then. 

## Outcomes
The implementation brings out the following salient aspects of this feature:
1. A Google Meet like professional interface to easily schedule meetings and add attendees
2. Ease of access to meetings and responding to meeting invites
3. Addition of meeting events to Google Calendar makes the user journey even more easy and professional

