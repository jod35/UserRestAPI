# User API
This is a simple REST API for users

# About the API

| ENDPOINT | HTTP VERB | ACTION |
|----------|-----------|--------|
|/users/   | GET       | get all users |
|/user/ID | GET       | get a single user by ID |
|/user/ID | PATCH    | update a user's info |
|/user/ID | DELETE  | delete a user  |
|/users/ |  POST   | create a new user |

### GET all users

```
[
 {"username":"user1",
   "email": "user1@test.com",
	 "password":"password"
 },
  {"username":"user2",
   "email": "user2@test.com",
     "password":"password"
   },  
]

```

That returns a list of resources


### GET a user by id

```
{"success":true,
  { "id":1
    "username":"user",
    "email":"user@test.com",
     "password":"password"
  }

}

```

This returns a user with an ID

### DELETE a user by ID

```
{
    "message": "User Deleted",
    "success": true,
    "user": {
        "email": "user@test.com",
        "id": 2,
        "password": "password",
        "username": "user"
    }
}




`i``
