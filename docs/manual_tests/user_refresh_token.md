## Manual testing for POST /user/refresh API

#### Dummy data used :
**username** : testrefresh, 
**password** : testrefresh@1234

* _Refresh token in Authorization field is the refresh token returned on login response_

    Refresh token returned on login response:
    
    _Screenshot_: 
    ![refreshToken](https://user-images.githubusercontent.com/50259869/94183019-6bdbd880-febf-11ea-8a8b-9d40c314cb4d.PNG)

    Entering the login response refresh token in the Authorization field:
    
    _Screenshot_: 
    ![](https://user-images.githubusercontent.com/50259869/94183020-6c746f00-febf-11ea-9e07-ba1c9436f965.PNG)
    ![](https://user-images.githubusercontent.com/50259869/94183022-6d0d0580-febf-11ea-8d5a-0eb67782a08c.PNG)

    _Expected Result_: SUCCESS

    _Actual Result_: SUCCESS

* _Refresh token in Authorization field is not valid or without Bearer_

    Filling refresh token in Authorization field without Bearer:

    _Screenshot:_
    ![](https://user-images.githubusercontent.com/50259869/94183024-6d0d0580-febf-11ea-8300-148cb647239d.PNG)
    ![](https://user-images.githubusercontent.com/50259869/94183026-6da59c00-febf-11ea-826a-584cd1659e16.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL

* _No Refresh token is given in the Authorization field after Bearer_

    Filling Authorization field with Bearer only and without refresh token:

    _Screenshot:_
    ![](https://user-images.githubusercontent.com/50259869/94183029-6da59c00-febf-11ea-95eb-1560dab180b0.PNG)
    ![](https://user-images.githubusercontent.com/50259869/94183030-6e3e3280-febf-11ea-8a25-f5bc6d464e3c.PNG)

    _Expected Result_: FAIL

    _Actual Result_: FAIL