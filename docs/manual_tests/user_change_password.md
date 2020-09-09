## manual_test for PUT /user/change_password


#### Dummy data used :
 **username** : test1234 , **password** : test@123


* _Change password to a different password from the current one_

    Change password from **test@123** to **Testing@1234**

     _Screenshot/gif_: 
    ![newPass](https://user-images.githubusercontent.com/64194946/92589746-a555f680-f2b8-11ea-8a90-8b551e03901b.png)

    ![newPassRes](https://user-images.githubusercontent.com/64194946/92589742-a424c980-f2b8-11ea-8172-4b436298f8f8.png)

     _Expected Result_: SUCCESS

     _Actual Result_: SUCCESS


* _Change password to a password equal to the current one_  

    Change password from **Testing@1234** to **Testing@1234**

     _Screenshot/gif_: 
     ![samePass](https://user-images.githubusercontent.com/64194946/92589723-9ff8ac00-f2b8-11ea-81c9-f66342d91f91.png)

     ![samePassRes](https://user-images.githubusercontent.com/64194946/92589718-9d965200-f2b8-11ea-9950-d50930447d5a.png)
      
     _Expected Result_: FAIL

     _Actual Result_: FAIL


* _Change password to an empty password_  

    Change password from **Testing@1234** to empty password.

     _Screenshot/gif_: 
      ![emptyPass](https://user-images.githubusercontent.com/64194946/92589739-a38c3300-f2b8-11ea-879e-24ad60b03ed9.png)

      ![emptyPassRes](https://user-images.githubusercontent.com/64194946/92589737-a2f39c80-f2b8-11ea-9fc5-9e12f25bb8a7.png)

     _Expected Result_: FAIL  

     _Actual Result_: FAIL


* _Change password to a password with white spaces_

    Change password from **Testing@1234** to **Test @1234**

     _Screenshot/gif_: 
      ![spacePass](https://user-images.githubusercontent.com/64194946/92589730-a25b0600-f2b8-11ea-8b3e-787641cb3c46.png)

      ![spacePassRes](https://user-images.githubusercontent.com/64194946/92589724-a129d900-f2b8-11ea-810e-84011147e8b7.png)

     _Expected Result_: FAIL 

     _Actual Result_: FAIL