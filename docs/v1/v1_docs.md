# WeAsk.Online API Documentation

<br/>

# Registration

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
<br/>
<br/>
<br/>

# Login
`POST /api/v1/login`

* To create a question, comment on a question, reply on a comment or vote, the user must be registered and already logged in.

### body
```
curl --location 'http://localhost:5000/api/v1/login' \
    --form 'username="user123"' \
    --form 'password="password@123"'
```

### Response
#### Success - 200 OK :

* On valid logging credentials, `api-token` set to users' cookie which is valid for 5 days and the following json will be responded.
```
{
    "api-token": "8db0c0d3-3d13-4a89-b577-941404c9e608",
    "message": "Success"
}
```

#### Error - 400 Bad Request :

* If required field is missing from the body
```
{
    "error": "Missing [fieldname]"
}
```

#### Error - 401 Unauthorized :

* Invalid username
```
{
    "error": "Invalid username"
}
```

* Incorrect password
```
{
    "error": "Incorrect password"
}
```

#### Error - 403 Forbidden :

* If the user account is banned or user deleted their account

```
{
    "error": "User account is inactive"
}
```

#### Error - 500 Server Error :

* If redis server is not running or failed
```
{
    "error": "Couldn't  connect to Redis server"
}
```
<br/>
<br/>
<br/>

# Create/Post Question
`POST /api/v1/questions`

* To create or post a new question, the user must be logged in and have the `api-token` in the request header

### body
```
curl --location 'http://localhost:5000/api/v1/questions' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data '{
        "title": string,
        "body": string,
        "tags": [string, string, ...]
    }'
```

### Response
#### Success - 201 Created :

* On valid post or creation of question
```
{
    'message': 'Question created'
}
```

#### Error - 401 Unauthorized

* If the `api-token` is not available in the request header or if the token is expired.

```
{
    "Error": "Not authorized"
}
```

#### Error - 400 Bad Request :

* If the `Content-Type` is not `application/json`
```
{
    'Error': 'Invalid JSON data'
}
```

* If Missing required field
```
{
    "Error": "Missing [fieldname]"
}
```


