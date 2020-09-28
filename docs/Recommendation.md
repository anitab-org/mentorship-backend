## RECOMMENDER SYSTEMS
As a contributor I have come up with a solution to make a recommender systems for the mentorship system in which mentees will be recommended to the mentors.<br>
Mentorship System is an application that allows women in tech to mentor each other, on career development topics,through 1:1 relations for a certain period. As we know that the mentorship can be provided on any career development topics but for the ease of explaining my concepts I have used topics which are basically programming languages that are being used in developement applications for mentorship systems.
<br>
There can be two methods to form the mentee-mentor DataFrame.The original dataset can be taken from the mentorship system database.

### FIRST METHOD
1. We will create a mentee Dataframe which basically contains the percentage of knowledge a particular mentee has on the given programming languages .If the mentee has not mentioned any knowledge level for any programming language then that has to be taken 0.But necessarily every mentee should have filled some knowledge percentage on the  given skills.Below is the sample Dataframe:-
<br>
![](photos/Screenshot%20(1032).png)
<br>
2.  In the same manner,We will create a mentor Dataframe which basically contains the percentage of knowledge a particular mentor has on the given programming languages .Given another point that a mentor should have around 50% of knowledge in atleast 2 topics .If the mentor has not mentioned any knowledge level for any programming language then that has to be taken 0.But necessarily every mentor should have filled some knowledge percentage on the  given skills.Below is the sample Dataframe:-
<br>
![](photos/Screenshot%20(1033).png)
<br>
3. Now we can create a mentor-mentee DataFrame by multiplication.Below is the sample DataFrame :-
<br>
![](photos/Screenshot%20(1035).png)
<br>

### SECOND METHOD

Mentees can give ratings to mentors under whom they have worked and vice-versa.Thereafter a dataframe can be created which contains the ratings.<br><br><br>
I thought of applying the first method as there are no current rating system available on any application.
After that standardized the values to a given range i.e 0 to 1.Because the percentages i.e the ratios  basically 
ranges from 0 to 1.
![](photos/Screenshot%20(1034).png)
After standardizing I used the cosine similarity function to find the correlation among the mentees so as to give required recommendation .
<br>
![](photos/Screenshot%20(1031).png)
<br>
I am using collaborative filtering method for recommender system . It is basically a user-user collaborative filtering which gives more accurate results . Below is the code of the recommender system.
<br>
![](photos/Screenshot%20(1036).png)
<br>
As we can see here that the mentees recommended here to the mentors in  they are weak particularly in areas where the mentors have good knowledge and have average or good knowledge at areas where the mentors have less knowledge in descending order so that they wouldn't face any issue overally.


