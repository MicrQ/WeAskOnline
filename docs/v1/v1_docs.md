## Registration

`POST /api/v1/register`

Used to register a new user.

### body
```
curl --location 'localhost:5000/api/v1/register' \
    --form 'firstname="John"' \
    --form 'lastname="Doe"' \
    --form 'username="John6"' \
    --form 'email="example@email.com"' \
    --form 'password="password@123"' \
    --form 'counrty="kenya"'
```

### Response
#### Success - 200 OK :
* On successful registration, the following response will be returned and the user is required to verify their email using the link value(url).
```
{
    "data": {
        "bio": "",
        "country_id": 87,
        "email": "example@email.com",
        "firstname": "john",
        "lastname": "doe",
        "username": "john6"
    },
    "link": "http://localhost:5000/api/v1/verify-email?key=ZXhhbXBsZUBlbWFpbC5jb20=",
    "message": "Success,user created. Please verifiy your email"
}
```

#### Error - 400 Bad Request :
* If not all required fields given
```
{
    "error": "Missing [field_name]
}
```
* If the country is not recognized
```
{
    "error": "Country not found"
}
```
* If email is not valid
```
{
    "error": "email not valid"
}
```

#### Error - 500 Server Error :
* If `Email` or `Password` for SMTP not found in environment variables.
```
{
    "error": "Server error, empty data found"
}
```


## Email Verification

`POST http://localhost:5000/api/v1/verify-email?key=ZXhhbXBsZUBlbWFpbC5jb20=`

* In order to be registered successfully, the user is required the verify their email using the like provided in the registration response.

### body
```
curl --location 'http://localhost:5000/api/v1/verify-email?key=ZXhhbXBsZUBlbWFpbC5jb20%3D' \
    --form 'otp="12345"'
```

### Response
#### Success - 200 OK :
* On valid email verification
```
{
    "message": "success, email verified"
}
```

#### Error - 400 Bad Request :
* If OTP is not valid
```
{
    "error": "Please, provide valid OTP"
}
```
* If Base64 encoded email of user is not available on the query parameter.
```
{
    "error": "Missing email address"
}
```

#### Error - 401 Unauthorized :
* If OTP expired or Invalid email
```
{
    "error": "token expired or invalid"
}
```

