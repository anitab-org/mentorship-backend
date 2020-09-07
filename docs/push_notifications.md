## Implementing Push Notifications

### Basic Steps

1. User gives the permission for push notifications on the client-side.
2. Client side generates a push subscription token by communication with the Push API.
3. Client service sends the subscription information to the backend service(this information should be persistent in the backend).
4. Backend push service initiates the push and send payload to the specific push service.
5. The push service receives the push notification and forwards it to the specific user.

### Implementation Details

1. Build a REST Interface which will communicate with the client application and push service. It will store subscription information of users and distribute Voluntary Application Server Identification (VAPID) public key.

2. The following API endpoints will be created:

``` 
/subscription/
GET – to get vapid public key
POST – to store subscription information

/push/
POST – will send push request to all users ( will be used for testing)
```

3. The pywebpush library is used for sending web push notification.

```Python
from pywebpush import webpush, WebPushException

def send_push_notifications(subscription_information, message_body):
    return webpush(
        subscription_info = subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY
    )

@app.route("/subscription",methods=["GET", "POST"])
def subscripion:
    """
    POST creates a subscription
    GET returns the VAPID key
    """
    if request.method == "GET":
        return Response(response=json.dumps({"public_key" : VAPID_PUBLIC}))
    
    if request.method == "POST":
        subscription_token = request.get_json("subscription_token")
        return Response(status=201,mimetype="application/json")

@app.route("/push_v1/", methods=['POST'])
def push_v1():
    message = "Push Test v1"
    print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed'})
    
    print("request.json",request.json)
    token = request.json.get('sub_token')

    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success'})
    except Exception as e:
        print("error",e)
        return jsonify({'failed' : str(e)})

```
The functions such as send_web_push() can be defined based on the requirements. The VAPID key is just a unique identification for each individual user, hence the API key can be used.

Services like DeleteSubscrption or adding certain groups for certain categories of push notifications can also be added to this particular API.

Some of the other endpoints that can be added are:

```
GET /v1/pushnotification
Will get a list of all the push notifications that are either scheduled for delivery or have been delivered to the users of your app.

POST /v1/pushnotification
Create a new push notification and schedule the notification for delivery.

DELETE /v1/pushnotification/{id}
Will delete a push notification matching the specified ID.

GET /v1/pushnotification/categories
Will get a list of all the available push notification categories for your app.

POST /v1/pushnotification/categories
Will create a new notifcation category that can be used to send notifications to specific user groups.

DELETE /v1/pushnotification/categories/{categoryId}
Will delete the notification category matching the specified ID.

PUT /v1/pushnotification/categories/{categoryId}
Will change the notification category matching the specified categoryId.
```

