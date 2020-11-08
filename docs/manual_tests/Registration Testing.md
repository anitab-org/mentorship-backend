# REGISTRATION TESTS

<h2>TEST-1</h2>
<h3>Test1 Description</h3>
  
#### *successfully creating an account with all the correct details*
   - name: "first test"  
   - username: "test_1"
   - password: "12345678"
   - email: "test_1@gmail.com"
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true
   
<h3>Screenshots</h3>  
  
<img src="https://user-images.githubusercontent.com/53532851/97424412-b0cbb280-1936-11eb-9ec8-829316ecb1b7.png" />
<img src="https://user-images.githubusercontent.com/53532851/97424743-2b94cd80-1937-11eb-9e18-a39bf2ece4ad.png" />

<h3>Expected Result: </h3> 
    
message: "User was created successfully"
  
success

<h3>Actual Result: </h3> 
  
message: "User was created successfully"
   
success

<h2>TEST-2</h2>
<h3>Test2 Description  </h3>

### *entering username which is already used*
   - name: "second test"  
   - `username: "test_1"`
   - password: "12345678"
   - email: "test_2@gmail.com"
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true

<h3>Screenshots</h3>  

<img src="https://user-images.githubusercontent.com/53532851/97424894-6139b680-1937-11eb-9582-2eb5cc5a02da.png" />
<img src="https://user-images.githubusercontent.com/53532851/97424933-6f87d280-1937-11eb-863d-7a26ca99f4db.png" />
  
<h3>Expected Result: </h3> 

message: "A user with that username already exists"

fail
  
<h3>Actual Result: </h3> 

message: "A user with that username already exists"

fail

<h2>TEST-3</h2>
<h3>Test3 Description </h3>

### *entering email which is already used*
   - name: "third test"  
   - username: "test_3"
   - password: "12345678"
   - `email: "test_1@gmail.com"`
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true

<h3>Screenshots</h3>  

<img src="https://user-images.githubusercontent.com/53532851/97425150-b70e5e80-1937-11eb-9542-293d23954b75.png" />
<img src="https://user-images.githubusercontent.com/53532851/97425197-c7bed480-1937-11eb-9658-c90a8daee23a.png" />
  
<h3>Expected Result: </h3> 

message: "A user with that email already exists"

fail
  
<h3>Actual Result : </h3> 

message: "A user with that email already exists"

fail

<h2>TEST-4</h2>
<h3>Test4 Description  </h3>

### *entering username with defying username length*
   - name: "fourth test"  
   - `username: "4"`
   - password: "12345678"
   - email: "test_4@gmail.com"
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true

<h3>Screenshots</h3>  

<img src="https://user-images.githubusercontent.com/53532851/97425455-27b57b00-1938-11eb-8ad4-7d8913a078a6.png" />
<img src="https://user-images.githubusercontent.com/53532851/97425501-356b0080-1938-11eb-8cfe-a7f3538e1d56.png" />
  
<h3>Expected Result : </h3> 

message: "the username field has to be longer than 4 characters and shorter than 26 characters"

fail
  
<h3>Actual Result : </h3> 

message: "the username field has to be longer than 4 characters and shorter than 26 characters"

fail

<h2>TEST-5</h2>
<h3>Test5 Description  </h3>

### *entering password with defying length*
   - name: "fifth test"  
   - username: "test-5"
   - `password: "123"`
   - email: "test_5@gmail.com"
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true

<h3>Screenshots</h3>  

<img src="https://user-images.githubusercontent.com/53532851/97425690-7236f780-1938-11eb-9314-fe8d31a16f00.png" />
<img src="https://user-images.githubusercontent.com/53532851/97425737-80851380-1938-11eb-8347-cb93b8b71e1d.png" />
  
<h3>Expected Result: </h3> 

message: "the password field has to be longer than 7 characters and shorter than 65 characters"

fail
  
<h3>Actual Result: </h3> 

message: "the username field has to be longer than 7 characters and shorter than 65 characters"

fail

<h2>TEST-6</h2>
<h3>Test6 Description </h3>
  
### *entering wrong email address*
   - name: "sixth test"  
   - username: "test-6"
   - password: "12345678"
   - `email: "test_6"`
   - terms_and_conditions_checked: true
   - need_mentoring: true
   - available_to_mentor: true

<h3>Screenshots</h3>  

<img src="https://user-images.githubusercontent.com/53532851/97426011-e1145080-1938-11eb-808e-e59ef752b226.png" />
<img src="https://user-images.githubusercontent.com/53532851/97426057-ea9db880-1938-11eb-918e-0682d5f6eeef.png" />
  
<h3>Expected Result: </h3> 

message: "your email is invalid"

fail
  
<h3>Actual Result : </h3> 

message: "your email is invalid"

fail
