# TESTS
**<h2>TEST-1</h2>**
  <h3>_Test1 Description_  </h3>
  
  
  *successfully creating an account with all the correct details*
 
 
   name: "first test"  
   
   username: "test_1"
   
   password: "12345678"
   
   email: "test_1@gmail.com"
   
   terms_and_conditions_checked: true
   
   need_mentoring: true
   
   
   available_to_mentor: true
   
   
  <h3>_Screenshots_</h3>  
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test1/Screenshot%202020-09-01%20at%2010.46.52%20AM.png?raw=true)
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test1/Screenshot%202020-09-01%20at%2010.47.35%20AM.png?raw=true)
  <br>
  <h3>_Expected Result_: </h3> account created successfully
  <h3>_Actual Result_:   </h3> account created successfully
  
  
  <br>
  
  
  <h2>TEST-2</h2>
  <h3>_Test2 Description_  </h3>
 
 *entering username which is already used*
 
 
   name: "second test"  
   
   username: "test_1"
   
   password: "12345678"
   
   email: "test_2@gmail.com"
   
   terms_and_conditions_checked: true
   
   need_mentoring: true
   
   
   available_to_mentor: true
   
   
  <h3>_Screenshots_</h3>  
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test2/Screenshot%202020-09-01%20at%2010.50.27%20AM.png?raw=true)
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test2/Screenshot%202020-09-01%20at%2010.50.42%20AM.png?raw=true)
  
  <br>
  
  <h3>_Expected Result_: </h3> 
  
  
  message: A user with that username already exists
  
  account creation failed
  <h3>_Actual Result_:   </h3> 
  
  
  message: A user with that username already exists
  
  account creation failed
  
   <br>
  <h2>TEST-3</h2>
  <h3>_Test3 Description_  </h3>
 
 
 *entering email which already used*
 
   name: "third test"  
   
   username: "test_3"
   
   password: "12345678"
   
   email: "test_1@gmail.com"
   
   terms_and_conditions_checked: true
   
   need_mentoring: true
   
   
   available_to_mentor: true
   
   
  <h3>_Screenshots_</h3>  
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test3/Screenshot%202020-09-01%20at%2010.52.08%20AM.png?raw=true)
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test3/Screenshot%202020-09-01%20at%2010.52.19%20AM.png?raw=true)
  <br>
  <h3>_Expected Result_: </h3> 
  
  message: A user with that email already exists
  
  account creation failed
  <h3>_Actual Result_:   </h3> 
  
  message: A user with that email already exists
  
  account creation failed
  
  
  <br>
   
  <h2>TEST-4</h2>
  <h3>_Test4 Description_  </h3>
 
 
 *entering username with defying username length*
 
   name: "fourth test"  
   
   username: "4"
   
   password: "12345678"
   
   email: "test_4@gmail.com"
   
   terms_and_conditions_checked: true
   
   need_mentoring: true
   
   
   available_to_mentor: true
   
   
  <h3>_Screenshots_</h3>  
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test4/Screenshot%202020-09-01%20at%2010.54.17%20AM.png?raw=true)
  
  
  ![Data entered](https://github.com/SHITIZ-AGGARWAL/mentorship-backend/blob/test/docs/manual_tests/screen%20shots/test4/Screenshot%202020-09-01%20at%2010.54.28%20AM.png?raw=true)
  <br>
  <h3>_Expected Result_: </h3> 
  
  message: the username field has to be longer than 4 characters and shorter than 26 characters
  
  account creation failed
  <h3>_Actual Result_:   </h3> 
  
  message: the username field has to be longer than 4 characters and shorter than 26 characters
  
  account creation failed
  
