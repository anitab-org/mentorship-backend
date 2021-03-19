## Manual testing for POST /user/refresh API

#### Dummy data used:
* **username**: refresh_test, 
* **password**: refresh_test@1234

* _Refresh using the expired token_

    Refresh token returned on login response:
    
    _Screenshot_: 
    ![loginOnce](https://user-images.githubusercontent.com/50259869/94347905-e0e11680-0055-11eb-8569-0249b45e52e6.PNG)

    Entering the expired login response refresh token in the Authorization field:
    
    _Screenshot_: 
    ![enterExpired](https://user-images.githubusercontent.com/56799401/102400371-d5273f80-4007-11eb-870e-b56b78a52eab.png)
    ![enterExpiredCurl](https://user-images.githubusercontent.com/50259869/94347907-e2124380-0055-11eb-982b-52e9f087540c.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _Refresh using new refresh token returned on login response_

    Login again to get a new refresh token:
    
    _Screenshot_: 
    ![loginAgain](https://user-images.githubusercontent.com/50259869/94347910-e2aada00-0055-11eb-982f-3919042cbac4.PNG)

    Entering the login response refresh token in the Authorization field:
    
    _Screenshot_: 
    ![correctToken](https://user-images.githubusercontent.com/56799401/102400371-d5273f80-4007-11eb-870e-b56b78a52eab.png)
    ![correctTokenCurl](https://user-images.githubusercontent.com/50259869/94347912-e3437080-0055-11eb-9912-452d4a637942.PNG)

    _Expected Result_: SUCCESS

    _Actual Result_: SUCCESS

* _Refresh token in Authorization field is not valid or without Bearer_

    Filling refresh token in Authorization field without Bearer:

    _Screenshot:_
    ![withoutBearer](https://user-images.githubusercontent.com/56799401/102400755-60a0d080-4008-11eb-87bb-713fc76f717c.png)
    ![withoutBearerCurl](https://user-images.githubusercontent.com/50259869/94347916-e4749d80-0055-11eb-8d40-94ed540ed33e.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _No Refresh token is given in the Authorization field after Bearer_

    Filling Authorization field with Bearer only and without refresh token:

    _Screenshot:_
    ![bearerOnly](https://user-images.githubusercontent.com/56799401/102400921-8c23bb00-4008-11eb-85c8-607e65649254.png)
    ![bearerOnlyCurl](https://user-images.githubusercontent.com/50259869/94347914-e3dc0700-0055-11eb-86cf-03789fff41a6.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _Single whitespace in Authorization field_

    Filling Authorization field with only a single whitespace:

    _Screenshot:_
    ![whitespaceOnly](https://user-images.githubusercontent.com/56799401/102401049-b8d7d280-4008-11eb-9f57-b5e56059300e.png)
    ![whitespaceOnlyCurl](https://user-images.githubusercontent.com/50259869/94347918-e5a5ca80-0055-11eb-93ec-6ce64c3e4f38.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL