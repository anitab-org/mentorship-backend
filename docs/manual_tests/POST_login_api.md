## Manual testing and report for POST /login API

### Test 1: Login as an already registered and verified User with the correct username and password

Username: Iam_tester <br>
Password: Earthismy@planet01

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/username.png)

_Expected Result_:  SUCCESS

_Actual Result_:    SUCCESS

### Test 2: Login as an already registered and verified User with correct email and password

Username: vovidi5873@hapremx.com <br>
Password: Earthismy@planet01

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/email.png)

_Expected Result_:  SUCCESS

_Actual Result_:    SUCCESS


### Test 3: Login as an already registered and verified User with correct username and wrong password

Username: Iam_tester <br>
Password: earthismy@planet001

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/wrongpassword1.png)

_Expected Result_:  SUCCESS

_Actual Result_:    SUCCESS


### Test 4: Login an already registered and verified User with correct email/ and wrong password

Username: vovidi5873@hapremx.com  <br>
Password: earthismy@planet001

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/wrongpassword2.png)

_Expected Result_:  SUCCESS

_Actual Result_:    SUCCESS


### Test 5: Login a User with non-existing email

Username : pjhjvs0gzq@just4fun.me <br>
Password : Itspassword@01

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/unregistered.png)

_Expected Result_:  SUCCESS

_Actual Result_:    **FAIL**

403:HTTPStatus.FORBIDDEN - Please register before login should be returned instead of 401:HTTPStatus.UNAUTHORIZED - Username or password is wrong 


### Test 6 : Login an already registered User with correct email and password, with email unverified

Username : rarzukotri@enayu.com <br>
Password : Itspassword@01

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/unverified.png)

_Expected Result_:  SUCCESS

_Actual Result_:    **FAIL**

403:HTTPStatus.FORBIDDEN - Please verify your email before login should be returned instead of 401:HTTPStatus.UNAUTHORIZED -Username or password is wrong 

### Test 7 : Login a User with non-existing username

Username : xoxo'sxoxo's/;  <br>
Password : Itspassword@01 

_Screenshot/gif_: ![alt](https://github.com/vj-codes/mentorship-backend/blob/login_apiOSH/docs/manual_tests/test_screenshot/nonexistingusername.png)

_Expected Result_:  SUCCESS

_Actual Result_:    **FAIL**

400:HTTPStatus.BAD_REQUEST - Invalid username should be returned instead of 401:HTTPStatus.UNAUTHORIZED -Username or password is wrong
