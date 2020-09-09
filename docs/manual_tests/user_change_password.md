## Manual Testing for PUT /user/change_password


#### Dummy data used :
 **username** : test1234 , **password** : test@123


* _Change password to a different password from the current one_

    Change password from **test@123** to **Testing@1234**

     _Screenshot_: 
    ![newPass](https://user-images.githubusercontent.com/64194946/92589746-a555f680-f2b8-11ea-8a90-8b551e03901b.png)

    ![newPassRes](https://user-images.githubusercontent.com/64194946/92589742-a424c980-f2b8-11ea-8172-4b436298f8f8.png)

     _Expected Result_: SUCCESS

     _Actual Result_: SUCCESS


* _Change password to a password equal to the current one_  

    Change password from **Testing@1234** to **Testing@1234**

     _Screenshot_: 
     ![samePass](https://user-images.githubusercontent.com/64194946/92589723-9ff8ac00-f2b8-11ea-81c9-f66342d91f91.png)

     ![samePassRes](https://user-images.githubusercontent.com/64194946/92589718-9d965200-f2b8-11ea-9950-d50930447d5a.png)
      
     _Expected Result_: FAIL

     _Actual Result_: FAIL


* _Change password to an empty password_  

    Change password from **Testing@1234** to empty password.

     _Screenshot_: 
      ![empty](https://user-images.githubusercontent.com/64194946/92595625-4b5a2e80-f2c2-11ea-8cbd-7696f38d4edc.png)

     _Expected Result_: FAIL  

     _Actual Result_: FAIL


* _Change password to a password with white spaces_

    Change password from **Testing@1234** to **Test@ 1234**

     _Screenshot_: 
      ![space](https://user-images.githubusercontent.com/64194946/92595820-92482400-f2c2-11ea-96d0-6cac0b8a343d.png)

     _Expected Result_: FAIL 

     _Actual Result_: FAIL