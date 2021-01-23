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
    ![enterExpired](https://user-images.githubusercontent.com/50259869/94347906-e179ad00-0055-11eb-9b37-1496638434a2.PNG)
    ![enterExpiredCurl](https://user-images.githubusercontent.com/50259869/94347907-e2124380-0055-11eb-982b-52e9f087540c.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _Refresh using new refresh token returned on login response_

    Login again to get a new refresh token:
    
    _Screenshot_: 
    ![loginAgain](https://user-images.githubusercontent.com/50259869/94347910-e2aada00-0055-11eb-982f-3919042cbac4.PNG)

    Entering the login response refresh token in the Authorization field:
    
    _Screenshot_: 
    ![correctToken](https://user-images.githubusercontent.com/50259869/94347911-e3437080-0055-11eb-9b52-1e2b014ed8b5.PNG)
    ![correctTokenCurl](https://user-images.githubusercontent.com/50259869/94347912-e3437080-0055-11eb-9912-452d4a637942.PNG)

    _Expected Result_: SUCCESS

    _Actual Result_: SUCCESS

* _Refresh token in Authorization field is not valid or without Bearer_

    Filling refresh token in Authorization field without Bearer:

    _Screenshot:_
    ![withoutBearer](https://user-images.githubusercontent.com/50259869/94347915-e4749d80-0055-11eb-97e3-6328a54fc399.PNG)
    ![withoutBearerCurl](https://user-images.githubusercontent.com/50259869/94347916-e4749d80-0055-11eb-8d40-94ed540ed33e.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _No Refresh token is given in the Authorization field after Bearer_

    Filling Authorization field with Bearer only and without refresh token:

    _Screenshot:_
    ![bearerOnly](https://user-images.githubusercontent.com/50259869/94347913-e3dc0700-0055-11eb-8ad9-3993edb31ea8.PNG)
    ![bearerOnlyCurl](https://user-images.githubusercontent.com/50259869/94347914-e3dc0700-0055-11eb-86cf-03789fff41a6.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _Single whitespace in Authorization field_

    Filling Authorization field with only a single whitespace:

    _Screenshot:_
    ![whitespaceOnly](https://user-images.githubusercontent.com/50259869/94347917-e50d3400-0055-11eb-98ad-a1dada8d5ba7.PNG)
    ![whitespaceOnlyCurl](https://user-images.githubusercontent.com/50259869/94347918-e5a5ca80-0055-11eb-93ec-6ce64c3e4f38.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL