* Test 1 : Email is sent to registered user's email.

     _Screenshot_: 

     ![test_1](https://user-images.githubusercontent.com/42766576/94338862-3f38d580-0013-11eb-8638-4ed46f4e9e13.png)


     _Expected Result_: SUCCESS (message: Check your email, a new verification email was sent.)

     _Actual Result_: SUCCESS (message: Check your email, a new verification email was sent.)


* Test 2:  Email is sent to the user who already confirmed their mail

     _Screenshot_: 

     ![test_2](https://user-images.githubusercontent.com/42766576/94338870-57a8f000-0013-11eb-8e83-1f1740242067.png)


     _Expected Result_:  FAILURE (message: You already confirm your email)

     _Actual Result_: FAILURE (message: You already confirm your email)


* Test 3:  Email is sent to an email that is not registered in the system

     _Screenshot_: 

    ![test_3](https://user-images.githubusercontent.com/42766576/94338843-14e71800-0013-11eb-9993-560d36527534.png)


     _Expected Result_:  FAILURE (message: You are not registered in the system.)

     _Actual Result_: FAILURE (message: You are not registered in the system.)
