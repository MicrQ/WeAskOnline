# WeAsk.Online API Documentation

<br/>

# Registration

`POST /api/v1/register`

Used to register a new user.

### body
```bash
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
```bash
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
```bash
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
```bash
curl --location 'http://localhost:5000/api/v1/questions' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data '{
        "title": string,
        "body": string,
        "tags": [string, string, ...]   # optional
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

<br/>
<br/>
<br/>

# Update/Put a question
`PUT /api/v1/questions/<int:id>`

* To update a question
### body
```bash
curl --location --request PUT 'http://localhost:5000/api/v1/questions/<int:id>' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data '{
        "title": string,
        "body": string,
        "tags": [string, string, ...]   # optional
    }'
```

### Response
#### Success - 200 OK :

* On valid update the following response will be sent.
```
{
    'message': 'Question updated'
}
```

#### Error - 401 Unauthorized :

* If the `api-token` is not found in the header or if the token is expired.
```
{
    "Error": "Not authorized"
}
```

#### Error - 403 Forbidden :

* If the user is NOT the owner of the question.
```
{
    'Error': 'You don\'t have permission to delete this question'
}
```

#### Error - 400 Bad Request :

* If the `Content-Type` is not `application/json`
```
{
    'Error': 'Invalid JSON data'
}
```

* If the required field is missing.
```
{
    "Error": "Missing [fieldname]"
}
```

#### Error - 404 Not Found :

* If the question with the given id is not found.
```
{
    "Error": "Not Found"
}
```

<br/>
<br/>
<br/>

# DELETE a question
`DELETE /api/v1/questions/<int:id>`

* To delete a question

### body
```bash
curl --location --request DELETE 'http://localhost:5000/api/v1/questions/<int:id>' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608'
```

### Response
#### Success - 200 OK :

* On successful deletion
```
{
    'message': 'Question deleted'
}
```

#### Error - 401 Unauthorized :
* If the `api-token` is not found in the header or if the token is expired.
```
{
    "Error": "Not authorized"
}
```

#### Error - 403 Forbidden :
* If the user is not the owner of the question
```
{
    'Error': 'You don\'t have permission to delete this question'
}
```
#### Error - 404 Not Found :
* If the question with the given Id is not found.
```
{
    "Error": "Not Found"
}
```

<br/>
<br/>
<br/>

# GET Questions
`GET /api/v1/questions`

* To get all questions

### body
```bash
curl --location 'http://localhost:5000/api/v1/questions' 
```

### Response
#### Success - 200 OK :

```
[
    {
        "body": "I Heard That Weask Online Is The Best Community To Learn. Can Anyone Tell Me More About That Platform Please.",
        "comments": 32,
        "created_at": "Tue, 17 Sep 2024 19:46:35 GMT",
        "downvotes": 2,
        "id": 2,
        "title": "What Is Weask.Online?",
        "updated_at": "Tue, 17 Sep 2024 19:46:35 GMT",
        "upvotes": 450,
        "user_id": 1
    },
    {
        "body": "I Want To Create A Simple Crud App With Python And Sqlite.",
        "comments": 16,
        "created_at": "Mon, 16 Sep 2024 10:43:00 GMT",
        "downvotes": 4,
        "id": 1,
        "title": "How To Use Flask With Sqlite?",
        "updated_at": "Mon, 16 Sep 2024 10:43:00 GMT",
        "upvotes": 24,
        "user_id": 1
    },
    .
    .
    .
]
```

<br />
<br />
<br />

# GET Question
`GET /api/v1/questions/<int:id>`
* To get single question

### body
```bash
curl --location 'http://localhost:5000/api/v1/questions/1'
```

### Response
#### Success - 302 Found :
* Will be redirected to `/api/v1/questions/<int:id>/<string:title>`
```
{
    "body": "I Want To Create A Simple Crud App With Python And Sqlite.",
    "comments": [
        {
            "body": "Pay for me and i will teach you!",
            "created_at": "Mon, 16 Sep 2024 11:05:35 GMT",
            "id": 1,
            "isEdited": false,
            "question_id": 1,
            "replies": [
                {
                    "body": "How much?",
                    "comment_id": 1,
                    "created_at": "Mon, 16 Sep 2024 11:38:11 GMT",
                    "id": 1,
                    "isEdited": false,
                    "user_id": 2,
                    "upvotes": 3,
                    "downvotes": 2
                },
                {
                    "body": "Why would i pay you?",
                    "comment_id": 1,
                    "created_at": "Mon, 16 Sep 2024 11:41:52 GMT",
                    "id": 2,
                    "isEdited": true,
                    "user_id": 3,
                    "upvotes": 4,
                    "downvotes: 1
                }
            ],
            "user_id": 1
        }
    ],
    "created_at": "Mon, 16 Sep 2024 10:43:00 GMT",
    "downvotes": 20,
    "id": 1,
    "title": "How To Use Flask With Sqlite?",
    "updated_at": "Mon, 16 Sep 2024 10:43:00 GMT",
    "upvotes": 5,
    "user_id": 1
}
```

#### Error - 404 Not Found :
* If the question with the given id is not found.

```
{
    "Error": "Not Found"
}
```

<br />
<br />
<br />


# Search for Question
`GET /api/v1/questions/search?q=<keyword>`

* To search for a question using a keyword from question titles.

### body
```bash
curl --location 'http://localhost:5000/api/v1/questions/search?q=weask'
```

### Response
#### Success - 200 OK :
```
[
    {
        "body": "I Heard That Weask Online Is The Best Community To Learn. Can Anyone Tell Me More About That Platform Please.",
        "created_at": "Tue, 17 Sep 2024 19:46:35 GMT",
        "id": 2,
        "title": "What Is Weask.Online?",
        "updated_at": "Tue, 17 Sep 2024 19:46:35 GMT",
        "user_id": 1
    },
    .
    .
    .
]
```

### Error - 404 Not Found :
* When the question with the given keyword is not found.

```
{
    "Error": "Not Found"
}
```

### Redirect - 302 Found :
* If the query parameter value is empty or not given, redirected to `/api/v1/questions`.
<br />
<br />
<br />

# Create/POST comment :
`POST /api/v1/questions/<int:question_id>/comments`
* To post a comment
### body
```bash
curl --location 'http://localhost:5000/api/v1/questions/1/comments' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data '{
        "body": "comment content"
    }'
```

### Response
#### Success - 201 Created :
* On valid comment creation
```
{
    'message': 'Success, comment created'
}
```

#### Error - 401 Unauthorized :
* If the `api-token` is not found in the header or if the token is expired.
```
{
    "Error": "Not authorized"
}
```


#### Error - 404 Not Found :
* If the question with the given id is not found.

```
{
    "Error": "Not Found"
}
```

#### Error - 400 Bad Request :
* If the `Content-Type` is not `application/json`
```json
{
    "error": "Invalid JSON data"
}
```

* If required field is missing
```json
{
    "error": "Missing comment body"
}
```

<br />
<br />
<br />

# Update/PUT comment:
`PUT /api/v1/questions/<int:question_id>/comments/<int:comment_id>`

* To update an existing comment.

### Body
```bash
curl --location --request PUT 'http://localhost:5000/api/v1/questions/1/comments/1' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --data-raw '{
        "body": "Updated comment content"
    }'
```

### Response
#### Success - 200 OK:

* On successful comment update.

```json
{
    "message": "Success, comment updated."
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found in the header or if the token is expired.

```json
{
    "Error": "Not authorized"
}
```

#### Errer - 403 Forbidden:
* If the user does not have permission to edit the comment.

```json
{
    "Error": "You don't have permission to edit this comment"
}
```

#### Error - 404 Not Found:

* If the question or the comment with the given id is not found.

```json
{
    "Error": "Not Found"
}
```

#### Error - 400 Bad Request:

* If the Content-Type is not application/json.

```json
{
    "error": "Invalid JSON data"
}
```

* If required fields are missing.

```json
{
    "error": "Missing comment body"
}
```

<br />
<br />
<br />

# DELETE comment:
`DELETE /api/v1/questions/<int:question_id>/comments/<int:comment_id>`

* To delete an existing comment if the user is the owner of the comment.

### Body
```bash
curl --location --request DELETE 'http://localhost:5000/api/v1/questions/1/comments/1' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608'
```

### Response
#### Success - 200 OK:

* On successful comment deletion.

```json
{
    "message": "Success, comment deleted"
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found in the header or if the token is expired.

```json
{
    "Error": "Not authorized"
}
```

#### Error - 403 Forbidden:

* If the user does not have permission to delete the comment.

``` json
{
    "Error": "You don't have permission to delete this comment"
}
```

#### Error - 404 Not Found:

* If the question or the comment with the given id is not found.

```json
{
    "Error": "Not Found"
}
```
<br/>
<br/>
<br/>

# Create/POST reply:
`POST /api/v1/comments/<int:comment_id>/reply`

* To create a new reply to a comment.

### Body
```bash
curl --location --request POST 'http://localhost:5000/api/v1/comments/1/reply' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "body": "This is a reply."
    }'
```

### Response
#### Success - 201 Created:

* On successful reply creation.

```json
{
    "message": "Reply created successfully."
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found in the header or if the token is expired.

```json
{
    "Error": "Not authorized"
}
```

#### Error - 404 Not Found:

* If the comment with the given comment_id is not found.

```json
{
    "Error": "Not Found"
}
```

### Error - 400 Bad Request:

* If the Content-Type is not application/json.

```json
{
    "Error": "Invalid JSON data"
}
```

* If the required field body is missing.

```json
{
    "Error": "Missing [fieldname]"
}
```
<br />
<br />
<br />

# Update/PUT reply:
`PUT /api/v1/comments/<int:comment_id>/reply/<int:reply_id>`

* To update an existing reply to a comment.

### Body
```bash
curl --location --request PUT 'http://localhost:5000/api/v1/comments/1/reply/1' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "body": "This is an updated reply."
    }'
```

### Response
#### Success - 200 OK:

* On successful update of the reply.

``` json
{
    "message": "Reply updated successfully."
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found in the header or if the token is expired.

```json
{
    "Error": "Not authorized"
}
```

#### Error - 404 Not Found:

* If the comment with the given comment_id is not found.

```json
{
    "Error": "Not Found"
}
```

* If the reply with the given reply_id is not found.

```json
{
    "Error": "Not Found"
}
```

#### Error - 403 Forbidden:

* If the current user does not have permission to update the reply.

```json
{
    "Error": "You don't have permission to update this reply."
}
```

#### Error - 400 Bad Request:

* If the Content-Type is not application/json.

```json
{
    "Error": "Invalid JSON data"
}
```

* If the required field body is missing.

```json
{
    "Error": "Missing body"
}
```

<br />
<br />
<br />

# DELETE reply:
`DELETE /api/v1/comments/<int:comment_id>/reply/<int:reply_id>`

* To delete an existing reply to a comment.

### Body
```bash
curl --location --request DELETE 'http://localhost:5000/api/v1/comments/1/reply/1' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608'
```

### Response
#### Success - 200 OK:

* On successful deletion of the reply.

```json
{
    "message": "Reply deleted successfully."
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found in the header or if the token is expired.

```json
{
    "Error": "Not authorized"
}
```

#### Error - 404 Not Found:

* If the comment with the given comment_id is not found.

```json
{
    "Error": "Not Found"
}
```

* If the reply with the given reply_id is not found.

```json
{
    "Error": "Not Found"
}
```
#### Error - 403 Forbidden:

* If the current user does not have permission to delete the reply.

```json
{
    "Error": "You don't have permission to delete this reply."
}
```

#### Error - 500 Internal Server Error:

* If the Redis server is unavailable.

```json
{
    "Error": "Redis server not available"
}
```

<br />
<br />
<br />

# Vote(Like/Dislike) on post:
`POST /api/v1/vote/<string:entity>/<int:id>`

* To create or update a vote for an entity (question, comment, or reply).

### Body
```bash
# to vote question
curl --location --request POST 'http://localhost:5000/api/v1/vote/question/1' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --data-raw '{
        "vote": "upvote"
    }'

# to vote comment
curl --location --request POST 'http://localhost:5000/api/v1/vote/comment/1' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --data-raw '{
        "vote": "downvote"
    }'

# to vote reply
curl --location --request POST 'http://localhost:5000/api/v1/vote/reply/1' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: api-token=8db0c0d3-3d13-4a89-b577-941404c9e608' \
    --data-raw '{
        "vote": "novote"
    }'
```

#### JSON Body Fields:

    vote (required): The type of vote, which can be one of:
        "upvote"
        "downvote"
        "novote" (to remove an existing vote)

### Response
#### Success - 200 OK:

* On successful creation or modification of the vote.

```json
{
    "message": "Success"
}
```

#### Error - 401 Unauthorized:

* If the api-token is not found or if the token is expired.

```json
{
    "error": "Not authorized"
}
```

#### Error - 404 Not Found:

* If the entity type is invalid (not a comment, question, or reply), or if the entity with the given id is not found.

``` json
{
    "error": "Not Found"
}
```
#### Error - 400 Bad Request:

* If the body is missing or malformed.

```json
{
    "error": "Empty body found"
}
```

* If the vote field is missing or invalid.

```json
{
    "error": "Missing vote entity"
}
```

* If an invalid vote type is provided.

```json
{
    "error": "Invalid vote entity"
}
```

#### Error - 500 Internal Server Error:

* If the Redis server is unavailable.

```json
{
    "error": "Redis server is not running"
}
```

<br />
<br />
<br />

# Get Tags:
`GET /api/v1/tags`

* Retrieves all available tags and returns them in JSON format along with the count of how many questions are associated with each tag.

### Response

#### Success - 200 OK:
* On successful retrieval of all tags, the response will include a list of tags, each with a `count` field that indicates how many times the tag is used.
```json
[
    {
        "id": 1,
        "name": "Python",
        "count": 10
    },
    {
        "id": 2,
        "name": "Flask",
        "count": 5
    },
    .
    .
    .
]
```

#### No Content - 204 No Content:

* If no tags are found in the database.

```json
{}
```

#### Error - 500 Internal Server Error:

* If an issue occurs while querying the database.

```json
{
    "error": "Internal Server Error"
}
```

<br/>
<br/>
<br/>
