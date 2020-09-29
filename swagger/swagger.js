var data = {
    
        "swagger": "2.0",
        "basePath": "/",
        "paths": {
            "/admin/new": {
                "post": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'User is now an Admin.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'User is already an Admin.'}"
                        }
                    },
                    "summary": "Assigns a User as a new Admin",
                    "description": "An existing admin can use this endpoint to designate another user as an admin.\nThis is done by passing \"user_id\" of that particular user.",
                    "operationId": "post_assign_new_user_admin",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Assign%20User%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Admins"
                    ]
                }
            },
            "/admin/remove": {
                "post": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': \"You don't have admin status. You can't revoke other admin user.\"}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'User is not an Admin.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'User admin status was revoked.'}"
                        }
                    },
                    "summary": "Revoke admin status from another User Admin",
                    "description": "An existing admin can use this endpoint to revoke admin status of another user.\nThis is done by passing \"user_id\" of that particular user.",
                    "operationId": "post_revoke_user_admin",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Assign%20User%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Admins"
                    ]
                }
            },
            "/admins": {
                "get": {
                    "responses": {
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'User is not an Admin.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "The token has expired! Please, login again or refresh it.<br>The token is invalid!<br>The authorization token is missing!"
                        },
                        "HTTPStatus.OK": {
                            "description": "Success.",
                            "schema": {
                                "$ref": "#/definitions/User%20list%20model"
                            }
                        }
                    },
                    "summary": "Returns all admin users",
                    "description": "A admin user with valid access token can view the list of all admins. The endpoint\ndoesn't take any other input. A JSON array having an object for each admin user is\nreturned. The array contains id, username, name, slack_username, bio,\nlocation, occupation, organization, skills.\nThe current admin user's details are not returned.",
                    "operationId": "get_list_of_admins",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Admins"
                    ]
                }
            },
            "/dashboard": {
                "get": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "User not found"
                        },
                        "HTTPStatus.OK": {
                            "description": "Successful response",
                            "schema": {
                                "$ref": "#/definitions/Get%20user%20dashboard"
                            }
                        }
                    },
                    "summary": "Get current User's dashboard",
                    "description": "Returns:\n    A dict containing user dashboard",
                    "operationId": "get_user_dashboard",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/home": {
                "get": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User not found.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "Successful response",
                            "schema": {
                                "$ref": "#/definitions/Get%20statistics%20on%20the%20app%20usage%20of%20the%20current%20user"
                            }
                        }
                    },
                    "summary": "Get Statistics regarding the current user",
                    "description": "Returns:\n    A dict containing user stats(name, pending_requests, accepted_requests,\n    completed_relations, cancelled_relations, rejected_requests, achievements)",
                    "operationId": "get_user_home_statistics",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/login": {
                "post": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'Username or password is wrong.'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'Please verify your email before login.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'The field username is missing.'}\n{'message': 'Password field is missing.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "Successful login",
                            "schema": {
                                "$ref": "#/definitions/Login%20response%20data%20model"
                            }
                        }
                    },
                    "summary": "Login user",
                    "description": "The user can login with (username or email) + password.\nUsername field can be either the User's username or the email.\nThe return value is an access token and the expiry timestamp.\nThe token is valid for 1 week.",
                    "operationId": "login",
                    "parameters": [
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Login%20request%20data%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/mentorship_relation/send_request": {
                "post": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'Mentor user does not exist.'}\n{'message': 'Mentee user does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'Your ID has to match either Mentor or Mentee IDs.'}\n{'message': 'You cannot have a mentorship relation with yourself.'}\n{'message': 'End date is invalid since date has passed.'}\n{'message': 'Mentorship relation maximum duration is 6 months.'}\n{'message': 'Mentorship relation minimum duration is 4 week.'}\n{'message': 'Mentor user is not available to mentor.'}\n{'message': 'Mentee user is not available to be mentored.'}\n{'message': 'Mentor user is already in a relationship.'}\n{'message': 'Mentee user is already in a relationship.'}\n{'message': 'Mentor ID field is missing.'}"
                        },
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'Mentorship relation was sent successfully.'}"
                        }
                    },
                    "summary": "Creates a new mentorship relation request",
                    "description": "Also, sends an email notification to the recipient about new relation request.\n\nInput:\n1. Header: valid access token\n2. Body: A dict containing\n- mentor_id, mentee_id: One of them must contain user ID\n- end_date: UNIX timestamp\n- notes: description of relation request\n\nReturns:\nSuccess or failure message. A mentorship request is send to the other\nperson whose ID is mentioned. The relation appears at /pending endpoint.",
                    "operationId": "send_request",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Send%20mentorship%20relation%20request%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{relation_id}/task/{task_id}/comment": {
                "parameters": [
                    {
                        "name": "relation_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "post": {
                    "responses": {
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'Task comment was created successfully.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'Comment field is missing.'}<br>{'message': 'Comment must be in string format.'}<br>{'message': 'The comment field has to be shorter than 401 characters.'}<br>{'message': 'This mentorship relation status is not in the accepted state.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}<br>{'message': 'The token is invalid!'}<br>{'message': 'The authorization token is missing!'}<br>{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}<br>{'message': 'Mentorship relation does not exist.'}<br>{'message': 'Task does not exist.'}"
                        }
                    },
                    "summary": "Creates a new task comment",
                    "operationId": "post_create_task_comment",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Task%20comment%20model."
                            }
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{relation_id}/task/{task_id}/comment/{comment_id}": {
                "parameters": [
                    {
                        "name": "relation_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "comment_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "put": {
                    "responses": {
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Task comment was updated successfully.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'Comment field is missing.'}<br>{'message': 'Comment must be in string format.'}<br>{'message': 'The comment field has to be shorter than 401 characters.'}<br>{'message': 'This mentorship relation status is not in the accepted state.'}<br>{'message': 'You have not created the comment and therefore cannot modify it.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}<br>{'message': 'The token is invalid!'}<br>{'message': 'The authorization token is missing!'}<br>{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}<br>{'message': 'Mentorship relation does not exist.'}<br>{'message': 'Task does not exist.'}<br>{'message': 'Task comment does not exist.'}<br>{'message': 'Task comment with given task id does not exist.'}"
                        }
                    },
                    "summary": "Modifies the task comment",
                    "operationId": "put_task_comment",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Task%20comment%20model."
                            }
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                },
                "delete": {
                    "responses": {
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Task comment was deleted successfully.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'This mentorship relation status is not in the accepted state.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}<br>{'message': 'The token is invalid!'}<br>{'message': 'The authorization token is missing!'}<br>{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'You have not created the comment and therefore cannot delete it.'}"
                        },
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}<br>{'message': 'Mentorship relation does not exist.'}<br>{'message': 'Task does not exist.'}<br>{'message': 'Task comment does not exist.'}<br>{'message': 'Task comment with given task id does not exist.'}"
                        }
                    },
                    "summary": "Deletes the task comment",
                    "operationId": "delete_task_comment",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{relation_id}/task/{task_id}/comments/": {
                "parameters": [
                    {
                        "name": "relation_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "get": {
                    "responses": {
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'This mentorship relation status is not in the accepted state.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}<br>{'message': 'The token is invalid!'}<br>{'message': 'The authorization token is missing!'}<br>{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}<br>{'message': 'Mentorship relation does not exist.'}<br>{'message': 'Task does not exist.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'List task comments from a mentorship relation with success.'}",
                            "schema": {
                                "$ref": "#/definitions/Task%20comments%20model."
                            }
                        }
                    },
                    "summary": "Lists the task comments",
                    "operationId": "get_task_comments",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "delete": {
                    "responses": {
                        "404": {
                            "description": "{'message': 'This mentorship relation request does not exist.'}"
                        },
                        "401": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "403": {
                            "description": "{'message': 'This mentorship relation is not in the pending state.'}\n{'message': 'You cannot delete a mentorship request that you did not create.'}"
                        },
                        "200": {
                            "description": "{'message': 'Mentorship relation was deleted successfully.'}"
                        }
                    },
                    "summary": "Delete a mentorship request",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of request which is to be deleted (request_id)\n\nReturns:\nSuccess or failure message.",
                    "operationId": "delete_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/accept": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "put": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'This mentorship relation request does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'This mentorship relation is not in the pending state.'}\n{'message': 'You cannot accept a mentorship request sent by yourself.'}\n{'message': 'You cannot accept a mentorship relation where you are not involved.'}\n{'message': 'You are currently involved in a mentorship relation.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Mentorship relation was accepted successfully.'}"
                        }
                    },
                    "summary": "Accept a mentorship relation",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of request which is to be accepted (request_id)\n\nReturns:\nSuccess or failure message.",
                    "operationId": "accept_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/cancel": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "put": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'This mentorship relation request does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'This mentorship relation status is not in the accepted state.'}\n{'message': 'You cannot cancel a mentorship relation where you are not involved.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Mentorship relation was cancelled successfully.'}"
                        }
                    },
                    "summary": "Cancel a mentorship relation",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of request which is to be cancelled (request_id)\n\nReturns:\nSuccess or failure message.",
                    "operationId": "cancel_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/reject": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "put": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'This mentorship relation request does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'This mentorship relation is not in the pending state.'}\n{'message': 'You cannot reject a mentorship request sent by yourself.'}\n{'message': 'You cannot reject a mentorship relation where you are not involved.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Mentorship relation was rejected successfully.'}"
                        }
                    },
                    "summary": "Reject a mentorship relation",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of request which is to be rejected (request_id)\n\nReturns:\nSuccess or failure message.",
                    "operationId": "reject_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/task": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "post": {
                    "responses": {
                        "403": {
                            "description": "{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'This mentorship relation status is not in the accepted state.'}"
                        },
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'Task was created successfully.'}"
                        }
                    },
                    "summary": "Create a task for a mentorship relation",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of request for which task is being created (request_id)\n3. Body: JSON object containing description of task.\n\nReturns:\nSuccess or failure message. It gets added to GET /tasks endpoint and\nis visible to the other person in the mentorship relation.",
                    "operationId": "create_task_in_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Create%20task%20request%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/task/{task_id}": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "delete": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'Mentorship relation does not exist.'}\n{'message': 'Task does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}\n{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Task was deleted successfully.'}"
                        }
                    },
                    "summary": "Delete a task",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of the task to be deleted (task_id) and it ID of the associated\nmentorship relation (request_id).\n3. Body: JSON object containing description of task.\n\nReturns:\nSuccess or failure message. Task is deleted if request is successful.",
                    "operationId": "delete_task_in_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/task/{task_id}/complete": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "put": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'Mentorship relation does not exist.'}\n{'message': 'Task does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}\n{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'Task was already achieved.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Task was achieved successfully.'}"
                        }
                    },
                    "summary": "Update a task to mark it as complate",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of task (task_id) and ID of the associated mentorship\nrelation (request_id). The user must be involved in this relation.\n3. Body:\n\nReturns:\nSuccess or failure message. The task is marked as complete if succesful.",
                    "operationId": "update_task_in_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relation/{request_id}/tasks": {
                "parameters": [
                    {
                        "name": "request_id",
                        "in": "path",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "get": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'Mentorship relation does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}\n{'message': 'You are not involved in this mentorship relation.'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "List tasks from a mentorship relation with success.",
                            "schema": {
                                "$ref": "#/definitions/List%20tasks%20response%20model"
                            }
                        }
                    },
                    "summary": "List all tasks from a mentorship relation",
                    "description": "Input:\n1. Header: valid access token\n2. Path: ID of the mentorship relation for which tasks are to be\ndisplayed(request_id). The user must be involved in this relation.\n\nReturns:\nJSON array containing task details as objects is displayed on success.",
                    "operationId": "list_tasks_in_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relations": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                                }
                            }
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "Return all user's mentorship relations, filtered by the relation state, was successfully.",
                            "schema": {
                                "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                            }
                        }
                    },
                    "summary": "Lists all mentorship relations of current user",
                    "description": "Input:\n1. Header: valid access token\n\nReturns:\nJSON array containing user's relations as objects.",
                    "operationId": "get_all_user_mentorship_relations",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "in": "query",
                            "description": "Mentorship relation state filter.",
                            "name": "relation_state",
                            "type": "string"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relations/current": {
                "get": {
                    "responses": {
                        "401": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "200": {
                            "description": "Returned current mentorship relation with success.",
                            "schema": {
                                "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                            }
                        }
                    },
                    "summary": "Lists current mentorship relation of the current user",
                    "description": "Input:\n1. Header: valid access token\n\nReturns:\nJSON array containing details of current mentorship relations as objects.",
                    "operationId": "get_current_mentorship_relation",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relations/past": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Returned past mentorship relations with success.",
                            "schema": {
                                "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                            }
                        },
                        "401": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        }
                    },
                    "summary": "Lists past mentorship relations of the current user",
                    "description": "Input:\n1. Header: valid access token\n\nReturns:\nJSON array containing details of past mentorship relations as objects.",
                    "operationId": "get_past_mentorship_relations",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/mentorship_relations/pending": {
                "get": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "200": {
                            "description": "Success",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                                }
                            }
                        },
                        "HTTPStatus.OK": {
                            "description": "Returned pending mentorship relation with success.",
                            "schema": {
                                "$ref": "#/definitions/List%20mentorship%20relation%20request%20model"
                            }
                        }
                    },
                    "summary": "Lists pending mentorship requests of the current user",
                    "description": "Input:\n1. Header: valid access token\n\nReturns:\nJSON array containing details of pending mentorship relations as objects.",
                    "operationId": "get_pending_mentorship_relations",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Mentorship Relation"
                    ]
                }
            },
            "/refresh": {
                "post": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "Successful refresh",
                            "schema": {
                                "$ref": "#/definitions/Refresh%20response%20data%20model"
                            }
                        }
                    },
                    "summary": "Refresh user's access",
                    "description": "The return value is an access token and the expiry timestamp.\nThe token is valid for 1 week.",
                    "operationId": "refresh",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/register": {
                "post": {
                    "responses": {
                        "HTTPStatus.CONFLICT": {
                            "description": "{'message': 'A user with that username already exists.'}\n{'message': 'A user with that email already exists.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'The username field has to be longer than 5 characters and shorter than 25 characters.'}\n{'message': 'The password field has to be longer than 8 characters and shorter than 64 characters.'}\n{'message': 'Your email is invalid.'}"
                        },
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'User was created successfully.A confirmation email has been sent via email. After confirming your email you can login.'}"
                        }
                    },
                    "summary": "Creates a new user",
                    "description": "The endpoint accepts details like name, username, password, email,\nterms_and_conditions_checked(true/false), need_mentoring(true/false),\navailable_to_mentor(true/false). A success message is displayed and\nverification email is sent to the user's email ID.",
                    "operationId": "create_user",
                    "parameters": [
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/User%20registration%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/user": {
                "put": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "Invalid input."
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'User was updated successfully.'}"
                        }
                    },
                    "summary": "Updates user profile",
                    "description": "A user with valid access token can use this endpoint to edit his/her own\nuser details. The endpoint takes any of the given parameters (name, username,\nbio, location, occupation, organization, slack_username, social_media_links,\nskills, interests, resume_url, photo_url, need_mentoring, available_to_mentor).\nThe response contains a success message.",
                    "operationId": "update_user_profile",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Update%20User%20request%20data%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                },
                "delete": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'User was deleted successfully.'}"
                        }
                    },
                    "summary": "Deletes user",
                    "description": "A user with valid access token can use this endpoint to delete his/her own\nuser details. The endpoint doesn't take any other input. The response contains\na success message.",
                    "operationId": "delete_user",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                },
                "get": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "200": {
                            "description": "Success",
                            "schema": {
                                "$ref": "#/definitions/User%20Complete%20model%20used%20in%20listing"
                            }
                        }
                    },
                    "summary": "Returns details of current user",
                    "description": "A user with valid access token can use this endpoint to view his/her own\nuser details. The endpoint doesn't take any other input.",
                    "operationId": "get_user",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/user/change_password": {
                "put": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "{'message': 'Current password is incorrect.'}"
                        },
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'Password was updated successfully.'}"
                        }
                    },
                    "summary": "Updates the user's password",
                    "description": "A user with valid access token can use this endpoint to change his/her own\npassword. The endpoint takes current password and new password as input.\nThe response contains a success message.",
                    "operationId": "update_user_password",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Change%20password%20request%20data%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/user/confirm_email/{token}": {
                "parameters": [
                    {
                        "in": "path",
                        "description": "Token sent to the user's email",
                        "name": "token",
                        "required": true,
                        "type": "string"
                    }
                ],
                "get": {
                    "responses": {
                        "HTTPStatus.CONFLICT": {
                            "description": "{'message': 'The confirmation link is invalid or the token has expired.'}"
                        },
                        "HTTPStatus.CREATED": {
                            "description": "{'message': 'User successfully created.'}\n{'message': 'You have confirmed your account. Thanks!'}"
                        }
                    },
                    "summary": "Confirms the user's account",
                    "description": "This endpoint is called when a new user clicks the verification link\nsent on the users' email. It takes the verification token through URL\nas input parameter.The verification token is valid for 24 hours. A success or\nfailure response is returned by the API.",
                    "operationId": "get_user_email_confirmation",
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/user/resend_email": {
                "post": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "{'message': 'You already confirm your email.'}"
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "Invalid input."
                        },
                        "HTTPStatus.OK": {
                            "description": "{'message': 'Check your email, a new verification email was sent.'}"
                        }
                    },
                    "summary": "Sends the user a new verification email",
                    "description": "This endpoint is called when a user wants the verification email to be\nresent. The verification token is valid for 24 hours. A success or\nfailure response is returned by the API.",
                    "operationId": "post_user_resend_email_confirmation",
                    "parameters": [
                        {
                            "name": "payload",
                            "required": true,
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/Resend%20email%20request%20data%20model"
                            }
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/users": {
                "get": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "The token has expired! Please, login again or refresh it.<br>The token is invalid!<br>The authorization token is missing!"
                        },
                        "200": {
                            "description": "Success",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/User%20list%20model"
                                }
                            }
                        }
                    },
                    "summary": "Returns list of all the users whose names contain the given query",
                    "description": "A user with valid access token can view the list of users. The endpoint\ndoesn't take any other input. A JSON array having an object for each user is\nreturned. The array contains id, username, name, slack_username, bio,\nlocation, occupation, organization, interests, skills, need_mentoring,\navailable_to_mentor. The current user's details are not returned.",
                    "operationId": "list_users",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "description": "Search query",
                            "name": "search",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "description": "specify page of users",
                            "name": "page",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "description": "specify number of users per page",
                            "name": "per_page",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/users/verified": {
                "get": {
                    "responses": {
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "The token has expired! Please, login again or refresh it.<br>The token is invalid!<br>The authorization token is missing!"
                        },
                        "200": {
                            "description": "Success",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/User%20list%20model"
                                }
                            }
                        }
                    },
                    "summary": "Returns all verified users whose names contain the given query",
                    "description": "A user with valid access token can view the list of verified users. The endpoint\ndoesn't take any other input. A JSON array having an object for each user is\nreturned. The array contains id, username, name, slack_username, bio,\nlocation, occupation, organization, interests, skills, need_mentoring,\navailable_to_mentor. The current user's details are not returned.",
                    "operationId": "get_verified_users",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        },
                        {
                            "description": "Search query",
                            "name": "search",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "description": "specify page of users",
                            "name": "page",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "description": "specify number of users per page",
                            "name": "per_page",
                            "type": "string",
                            "in": "query"
                        },
                        {
                            "name": "X-Fields",
                            "in": "header",
                            "type": "string",
                            "format": "mask",
                            "description": "An optional fields mask"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            },
            "/users/{user_id}": {
                "parameters": [
                    {
                        "in": "path",
                        "description": "The user identifier",
                        "name": "user_id",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "get": {
                    "responses": {
                        "HTTPStatus.NOT_FOUND": {
                            "description": "{'message': 'User does not exist.'}"
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "{'message': 'The token has expired! Please, login again or refresh it.'}\n{'message': 'The token is invalid!'}\n{'message': 'The authorization token is missing!'}"
                        },
                        "HTTPStatus.OK": {
                            "description": "Success.",
                            "schema": {
                                "$ref": "#/definitions/User%20list%20model"
                            }
                        }
                    },
                    "summary": "Returns a user",
                    "description": "A user with valid access token can view the details of another user. The endpoint\ntakes \"user_id\" of such user has input.",
                    "operationId": "get_user",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": true,
                            "description": "Authentication access token. E.g.: Bearer <access_token>"
                        }
                    ],
                    "tags": [
                        "Users"
                    ]
                }
            }
        },
        "info": {
            "title": "Mentorship System API",
          "version": "1.0",
          "description": "API documentation for the backend of Mentorship System. \n \nMentorship System is an application that matches women in tech to mentor each other, on career development, through 1:1 relations during a certain period of time. \n \nThe main repository of the Backend System can be found here: https://github.com/anitab-org/mentorship-backend \n \nThe Android client for the Mentorship System can be found here: https://github.com/anitab-org/mentorship-android \n \nFor more information about the project here's a link to our wiki guide: https://github.com/anitab-org/mentorship-backend/wiki \n \nThis <a href=https://github.com/anitab-org/mentorship-backend/blob/develop/docs/quality-assurance-test-cases.md>Quality Assurance Test cases</a> document contains examples of test scenarios to evaluate if the API is working as it should."
           },
           "produces": [
        "application/json"
    ],
    "consumes": [
        "application/json"
    ],
    "tags": [
        {
            "name": "Users",
            "description": "Operations related to users"
        },
        {
            "name": "Admins",
            "description": "Operations related to Admin users"
        },
        {
            "name": "Mentorship Relation",
            "description": "Operations related to mentorship relations between users"
        }
    ],
    "definitions": {
        "User list model": {
            "required": [
                "bio",
                "location",
                "name",
                "occupation",
                "organization",
                "skills",
                "slack_username",
                "username"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The unique identifier of a user"
                },
                "username": {
                    "type": "string",
                    "description": "User username"
                },
                "name": {
                    "type": "string",
                    "description": "User name"
                },
                "slack_username": {
                    "type": "string",
                    "description": "User Slack username"
                },
                "bio": {
                    "type": "string",
                    "description": "User bio"
                },
                "location": {
                    "type": "string",
                    "description": "User location"
                },
                "occupation": {
                    "type": "string",
                    "description": "User occupation"
                },
                "organization": {
                    "type": "string",
                    "description": "User organization"
                },
                "skills": {
                    "type": "string",
                    "description": "User skills"
                }
            },
            "type": "object"
        },
        "Update User request data model": {
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User name"
                },
                "username": {
                    "type": "string",
                    "description": "User username"
                },
                "bio": {
                    "type": "string",
                    "description": "User bio"
                },
                "location": {
                    "type": "string",
                    "description": "User location"
                },
                "occupation": {
                    "type": "string",
                    "description": "User occupation"
                },
                "organization": {
                    "type": "string",
                    "description": "User organization"
                },
                "slack_username": {
                    "type": "string",
                    "description": "User slack username"
                },
                "social_media_links": {
                    "type": "string",
                    "description": "User social media links"
                },
                "skills": {
                    "type": "string",
                    "description": "User skills"
                },
                "interests": {
                    "type": "string",
                    "description": "User interests"
                },
                "resume_url": {
                    "type": "string",
                    "description": "User resume url"
                },
                "photo_url": {
                    "type": "string",
                    "description": "User photo url"
                },
                "need_mentoring": {
                    "type": "boolean",
                    "description": "User need mentoring indication"
                },
                "available_to_mentor": {
                    "type": "boolean",
                    "description": "User availability to mentor indication"
                }
            },
            "type": "object"
        },
        "User Complete model used in listing": {
            "required": [
                "email",
                "is_admin",
                "is_email_verified",
                "name",
                "password_hash",
                "registration_date",
                "terms_and_conditions_checked",
                "username"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The unique identifier of a user"
                },
                "name": {
                    "type": "string",
                    "description": "User name"
                },
                "username": {
                    "type": "string",
                    "description": "User username"
                },
                "email": {
                    "type": "string",
                    "description": "User email"
                },
                "password_hash": {
                    "type": "string",
                    "description": "User password hash"
                },
                "terms_and_conditions_checked": {
                    "type": "boolean",
                    "description": "User Terms and Conditions check state"
                },
                "is_admin": {
                    "type": "boolean",
                    "description": "User admin status"
                },
                "registration_date": {
                    "type": "number",
                    "description": "User registration date"
                },
                "is_email_verified": {
                    "type": "boolean",
                    "description": "User email verification status"
                },
                "email_verification_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "User email verification date"
                },
                "bio": {
                    "type": "string",
                    "description": "User bio"
                },
                "location": {
                    "type": "string",
                    "description": "User location"
                },
                "occupation": {
                    "type": "string",
                    "description": "User occupation"
                },
                "organization": {
                    "type": "string",
                    "description": "User organization"
                },
                "slack_username": {
                    "type": "string",
                    "description": "User slack username"
                },
                "social_media_links": {
                    "type": "string",
                    "description": "User social media links"
                },
                "skills": {
                    "type": "string",
                    "description": "User skills"
                },
                "interests": {
                    "type": "string",
                    "description": "User interests"
                },
                "resume_url": {
                    "type": "string",
                    "description": "User resume url"
                },
                "photo_url": {
                    "type": "string",
                    "description": "User photo url"
                },
                "need_mentoring": {
                    "type": "boolean",
                    "description": "User need mentoring indication"
                },
                "available_to_mentor": {
                    "type": "boolean",
                    "description": "User availability to mentor indication"
                },
                "current_mentorship_role": {
                    "type": "integer",
                    "description": "User current role"
                },
                "membership_status": {
                    "type": "integer",
                    "description": "User membershipstatus"
                }
            },
            "type": "object"
        },
        "Change password request data model": {
            "required": [
                "current_password",
                "new_password"
            ],
            "properties": {
                "current_password": {
                    "type": "string",
                    "description": "User's current password"
                },
                "new_password": {
                    "type": "string",
                    "description": "User's new password"
                }
            },
            "type": "object"
        },
        "User registration model": {
            "required": [
                "email",
                "name",
                "password",
                "terms_and_conditions_checked",
                "username"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User name"
                },
                "username": {
                    "type": "string",
                    "description": "User username"
                },
                "password": {
                    "type": "string",
                    "description": "User password"
                },
                "email": {
                    "type": "string",
                    "description": "User email"
                },
                "terms_and_conditions_checked": {
                    "type": "boolean",
                    "description": "User check Terms and Conditions value"
                },
                "need_mentoring": {
                    "type": "boolean",
                    "description": "User need mentoring indication"
                },
                "available_to_mentor": {
                    "type": "boolean",
                    "description": "User availability to mentor indication"
                }
            },
            "type": "object"
        },
        "Resend email request data model": {
            "required": [
                "email"
            ],
            "properties": {
                "email": {
                    "type": "string",
                    "description": "User's email"
                }
            },
            "type": "object"
        },
        "Refresh response data model": {
            "required": [
                "access_expiry",
                "access_token"
            ],
            "properties": {
                "access_token": {
                    "type": "string",
                    "description": "User's access token"
                },
                "access_expiry": {
                    "type": "number",
                    "description": "Access token expiry UNIX timestamp"
                }
            },
            "type": "object"
        },
        "Login request data model": {
            "required": [
                "password",
                "username"
            ],
            "properties": {
                "username": {
                    "type": "string",
                    "description": "User's username"
                },
                "password": {
                    "type": "string",
                    "description": "User's password"
                }
            },
            "type": "object"
        },
        "Login response data model": {
            "required": [
                "access_expiry",
                "access_token",
                "refresh_expiry",
                "refresh_token"
            ],
            "properties": {
                "access_token": {
                    "type": "string",
                    "description": "User's access token"
                },
                "access_expiry": {
                    "type": "number",
                    "description": "Access token expiry UNIX timestamp"
                },
                "refresh_token": {
                    "type": "string",
                    "description": "User's refresh token"
                },
                "refresh_expiry": {
                    "type": "number",
                    "description": "Refresh token expiry UNIX timestamp"
                }
            },
            "type": "object"
        },
        "Get statistics on the app usage of the current user": {
            "required": [
                "accepted_requests",
                "cancelled_relations",
                "completed_relations",
                "name",
                "pending_requests",
                "rejected_requests"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the user"
                },
                "pending_requests": {
                    "type": "integer",
                    "description": "Number of pending requests"
                },
                "accepted_requests": {
                    "type": "integer",
                    "description": "Number of accepted requests"
                },
                "completed_relations": {
                    "type": "integer",
                    "description": "Number of completed relations"
                },
                "cancelled_relations": {
                    "type": "integer",
                    "description": "Number of cancelled relations"
                },
                "rejected_requests": {
                    "type": "integer",
                    "description": "Number of rejected relations"
                },
                "achievements": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List tasks response model"
                    }
                }
            },
            "type": "object"
        },
        "List tasks response model": {
            "required": [
                "created_at",
                "description",
                "id",
                "is_done"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Task ID"
                },
                "description": {
                    "type": "string",
                    "description": "Mentorship relation task description"
                },
                "is_done": {
                    "type": "boolean",
                    "description": "Mentorship relation task is done indication"
                },
                "created_at": {
                    "type": "number",
                    "description": "Task creation date in UNIX timestamp format"
                },
                "completed_at": {
                    "type": "number",
                    "description": "Task completion date in UNIX timestamp format"
                }
            },
            "type": "object"
        },
        "Get user dashboard": {
            "properties": {
                "as_mentor": {
                    "$ref": "#/definitions/Get received and sent relations"
                },
                "as_mentee": {
                    "$ref": "#/definitions/Get received and sent relations"
                },
                "tasks_todo": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List tasks response model"
                    }
                },
                "tasks_done": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List tasks response model"
                    }
                }
            },
            "type": "object"
        },
        "Get received and sent relations": {
            "properties": {
                "sent": {
                    "$ref": "#/definitions/relations by state"
                },
                "received": {
                    "$ref": "#/definitions/relations by state"
                }
            },
            "type": "object"
        },
        "relations by state": {
            "properties": {
                "accepted": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List mentorship relation request model for user dashboard"
                    }
                },
                "rejected": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List mentorship relation request model for user dashboard"
                    }
                },
                "completed": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List mentorship relation request model for user dashboard"
                    }
                },
                "cancelled": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List mentorship relation request model for user dashboard"
                    }
                },
                "pending": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/List mentorship relation request model for user dashboard"
                    }
                }
            },
            "type": "object"
        },
        "List mentorship relation request model for user dashboard": {
            "required": [
                "accept_date",
                "action_user_id",
                "creation_date",
                "end_date",
                "id",
                "notes",
                "start_date",
                "state"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Mentorship relation ID"
                },
                "action_user_id": {
                    "type": "integer",
                    "description": "Mentorship relation requester user ID"
                },
                "mentor": {
                    "$ref": "#/definitions/user details for dashboard"
                },
                "mentee": {
                    "$ref": "#/definitions/user details for dashboard"
                },
                "creation_date": {
                    "type": "number",
                    "description": "Mentorship relation creation date in UNIX timestamp format"
                },
                "accept_date": {
                    "type": "number",
                    "description": "Mentorship relation acceptance date in UNIX timestamp format"
                },
                "start_date": {
                    "type": "number",
                    "description": "Mentorship relation start date in UNIX timestamp format"
                },
                "end_date": {
                    "type": "number",
                    "description": "Mentorship relation end date in UNIX timestamp format"
                },
                "state": {
                    "type": "integer",
                    "description": "Mentorship relation state"
                },
                "notes": {
                    "type": "string",
                    "description": "Mentorship relation notes"
                }
            },
            "type": "object"
        },
        "user details for dashboard": {
            "required": [
                "id",
                "photo_url",
                "user_name"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "user ID"
                },
                "user_name": {
                    "type": "string",
                    "description": "Mentorship relation user name"
                },
                "photo_url": {
                    "type": "string",
                    "description": "Mentorship relation user profile picture URL"
                }
            },
            "type": "object"
        },
        "Assign User model": {
            "required": [
                "user_id"
            ],
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The unique identifier of a user"
                }
            },
            "type": "object"
        },
        "Send mentorship relation request model": {
            "required": [
                "end_date",
                "mentee_id",
                "mentor_id",
                "notes"
            ],
            "properties": {
                "mentor_id": {
                    "type": "integer",
                    "description": "Mentorship relation mentor ID"
                },
                "mentee_id": {
                    "type": "integer",
                    "description": "Mentorship relation mentee ID"
                },
                "end_date": {
                    "type": "number",
                    "description": "Mentorship relation end date in UNIX timestamp format"
                },
                "notes": {
                    "type": "string",
                    "description": "Mentorship relation notes"
                }
            },
            "type": "object"
        },
        "List mentorship relation request model": {
            "required": [
                "accept_date",
                "action_user_id",
                "creation_date",
                "end_date",
                "id",
                "notes",
                "sent_by_me",
                "start_date",
                "state"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Mentorship relation ID"
                },
                "action_user_id": {
                    "type": "integer",
                    "description": "Mentorship relation requester user ID"
                },
                "sent_by_me": {
                    "type": "boolean",
                    "description": "Mentorship relation sent by current user indication"
                },
                "mentor": {
                    "$ref": "#/definitions/User"
                },
                "mentee": {
                    "$ref": "#/definitions/User"
                },
                "creation_date": {
                    "type": "number",
                    "description": "Mentorship relation creation date in UNIX timestamp format"
                },
                "accept_date": {
                    "type": "number",
                    "description": "Mentorship relation acceptance date in UNIX timestamp format"
                },
                "start_date": {
                    "type": "number",
                    "description": "Mentorship relation start date in UNIX timestamp format"
                },
                "end_date": {
                    "type": "number",
                    "description": "Mentorship relation end date in UNIX timestamp format"
                },
                "state": {
                    "type": "integer",
                    "description": "Mentorship relation state"
                },
                "notes": {
                    "type": "string",
                    "description": "Mentorship relation notes"
                }
            },
            "type": "object"
        },
        "User": {
            "required": [
                "id",
                "name"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "User ID"
                },
                "name": {
                    "type": "string",
                    "description": "User name"
                }
            },
            "type": "object"
        },
        "Create task request model": {
            "required": [
                "description"
            ],
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Mentorship relation task description"
                }
            },
            "type": "object"
        },
        "Task comment model.": {
            "required": [
                "comment"
            ],
            "properties": {
                "comment": {
                    "type": "string",
                    "description": "Task comment."
                }
            },
            "type": "object"
        },
        "Task comments model.": {
            "required": [
                "comment",
                "creation_date",
                "id",
                "relation_id",
                "task_id",
                "user_id"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Task comment's id."
                },
                "user_id": {
                    "type": "integer",
                    "description": "User's id."
                },
                "task_id": {
                    "type": "integer",
                    "description": "Task's id."
                },
                "relation_id": {
                    "type": "integer",
                    "description": "Relation's id."
                },
                "creation_date": {
                    "type": "number",
                    "description": "Creation date of the task comment."
                },
                "modification_date": {
                    "type": "number",
                    "description": "Modification date of the task comment."
                },
                "comment": {
                    "type": "string",
                    "description": "Task comment."
                }
            },
            "type": "object"
        }
    },
    "responses": {
        "ParseError": {
            "description": "When a mask can't be parsed"
        },
        "MaskError": {
            "description": "When any error occurs on mask"
        },
        "NoAuthorizationError": {},
        "CSRFError": {},
        "ExpiredSignatureError": {},
        "InvalidHeaderError": {},
        "InvalidTokenError": {},
        "JWTDecodeError": {},
        "WrongTokenError": {},
        "RevokedTokenError": {},
        "FreshTokenRequired": {},
        "UserLoadError": {},
        "UserClaimsVerificationError": {}
    }
           
}
document.getElementById("container").appendChild(
    renderjson(data)
);
