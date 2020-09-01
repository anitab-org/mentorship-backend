# Manual Testing for PUT/user and PUT/user/change_password

Created the following users :
1. ***name:*** yash , ***username:*** cali123 and ***password:*** cali1234567@
2. ***name:*** john , ***username:*** bo123 and ***password:*** semrush2189@ 

* _TBD(Change existing username to a different username)_ 
     
     Changed the username from cali123 to opt124
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/tbd.PNG)
     _Expected Result_:  SUCCESS
     
     _Actual Result_:    SUCCESS


* _Change username to a username already being used by another User_ 
     
     Tried changing the username cali123 to bo123. Since this username already exists for the name john, it failed to update username.
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/Capture.PNG)
     
     _Expected Result_:  FAIL
     
     _Actual Result_:    FAIL
     
 
 * _Change password to a different password from the current one	_ 
     
     Tried changing the password for the username bo123. The new password is Semrush2189@
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/passwd.PNG)
     
     _Expected Result_:  SUCCESS
     
     _Actual Result_:    SUCCESS
     
     
 * _Change password to a password equal to the current one_ 
     
     Tried changing the password for the username bo123. The new password was set the same as the current one(i.e. Semrush2189@)
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/samepass.PNG)
     
     _Expected Result_:  FAIL
     
     _Actual Result_:    FAIL
     
  
  * _Change password to an empty password_ 
     
     Tried changing the password for the username bo123.The new password was left empty.
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/emptpass.PNG)
     
     _Expected Result_:  FAIL
     
     _Actual Result_:    FAIL
     
     
   * _Change password to a password with white spaces_ 
     
     Tried changing the password for the username bo123.The new password was given white space.
     
     _Screenshot_:  ![alt text](https://github.com/yash2189/mentorship-backend/blob/develop/test%20screenshots/whitespacepass.PNG)
     
     _Expected Result_:  FAIL
     
     _Actual Result_:    FAIL
