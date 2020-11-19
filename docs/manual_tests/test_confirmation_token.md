* Test 1 : Verification token entered is one sent on user's registered email within 24 hrs

     _Screenshot/gif_: 
     
     ![test_1](https://user-images.githubusercontent.com/56037184/94105745-91cd9280-fe57-11ea-90e7-6e514cb3ada2.png)


     _Expected Result_: SUCCESS (message: You have confirmed your account. Thanks!)

     _Actual Result_: SUCCESS (message: You have confirmed your account. Thanks!)


* Test 2:  Verification token of already confirmed users account entered

     _Screenshot/gif_: 
     
     ![test_2](https://user-images.githubusercontent.com/56037184/94105790-a90c8000-fe57-11ea-8044-aee26039567e.png)


     _Expected Result_:  SUCCESS (message: Account already confirmed)

     _Actual Result_: SUCCESS (message: Account already confirmed)


* Test 3:  Verification token of un-confirmed users account entered after 24 hrs of email being sent

     _Screenshot/gif_: 
     
    ![test_3](https://user-images.githubusercontent.com/56037184/94105821-bf1a4080-fe57-11ea-9f9f-2d895a62fffb.png)


     _Expected Result_:  Failure (message: The confirmation link is invalid or the token has expired.)

     _Actual Result_: SUCCESS (message: You have confirmed your account. Thanks!)

    _Reason_: I tested it and it is valid for 30days.


* Test 4:  Incorrect verification token entered in request body

     _Screenshot/gif_: 
     
    ![test_4](https://user-images.githubusercontent.com/56037184/94105890-e83ad100-fe57-11ea-92c9-95951ae57bb1.png)


     _Expected Result_:  Failure (message: The confirmation link is invalid or the token has expired.)

     _Actual Result_: FAILURE (message: The confirmation link is invalid or the token has expired.)
