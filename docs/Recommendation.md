## RECOMMENDER SYSTEMS
As a contributor, I have come up with a solution to make a recommender system for the mentorship system in which mentees will be recommended to the mentors.  
Mentorship System is an application that allows women in tech to mentor each other, on career development topics, through 1:1 relations for a certain period. We know that mentorship can be provided on any career development topics but for the ease of explaining my concepts, I have taken topics that are programming languages that are being used in developing applications for mentorship systems.   
There can be two methods to form the mentee-mentor DataFrame.The original dataset can be taken from the mentorship system database.
### FIRST METHOD
1. We will create a mentee data frame that contains the percentage of knowledge a particular mentee has on the given programming languages. If a mentee has not mentioned his/her knowledge level for the given programming languages then that has to be taken as `0`. But necessarily every mentee should have filled some knowledge percentage for the given programming languages.   
Below is the sample Dataframe:-   
![Screenshot (1032)](https://user-images.githubusercontent.com/48198809/97035787-79e74c80-1584-11eb-86bd-6970f54bca9a.png)
2.  In the same manner, We will create a mentor Dataframe that contains the percentage of knowledge a particular mentor has on the given programming languages. Given another point that a mentor should have around 50% of knowledge in at least `2` topics. If the mentor has not mentioned any knowledge level for any given programming languages then that has to be taken `0`. But necessarily every mentor should have filled some knowledge percentage for the given programming languages. Below is the sample Dataframe:-    
![Screenshot (1033)](https://user-images.githubusercontent.com/48198809/97035869-98e5de80-1584-11eb-84a8-4c2910e58559.png)
3. We now create a mentor-mentee DataFrame by multiplication. Below is the sample DataFrame:-    
![Screenshot (1035)](https://user-images.githubusercontent.com/48198809/97035882-9edbbf80-1584-11eb-97bf-41109eef6c58.png)
### SECOND METHOD
Mentees can give ratings to mentors under whom they have worked and vice-versa. Thereafter a data frame can be created which contains the ratings.
I thought of applying the first method as there is no current rating system available on any application.
After that, I standardized the values to a given range from `0` to `1` because the ratio ranges from `0` to `1`.
![Screenshot (1034)](https://user-images.githubusercontent.com/48198809/97035875-9be0cf00-1584-11eb-8839-a511b8704622.png)   
After standardizing, I used the cosine similarity function to find the correlation among the mentees to give the required recommendation.
![Screenshot (1031)](https://user-images.githubusercontent.com/48198809/97035706-5ae8ba80-1584-11eb-889b-3a76500826c9.png)     
I am using a collaborative filtering method for the recommender system. It is basically user-user collaborative filtering that gives more accurate results. Below is the code of the recommender system.
![Screenshot (1036)](https://user-images.githubusercontent.com/48198809/97035893-a13e1980-1584-11eb-96c8-912dcfe84c8e.png)    
As we can see here that the mentees recommended here to the mentors they are weak particularly in areas where the mentors have good knowledge and have an average or good knowledge at areas where the mentors have less knowledge in descending order so that they wouldn't face any issue overall.