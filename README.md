# Supporting Clever Instant Login in Flask
[Clever APIs](https://dev.clever.com/) empower developers and school districts everywhere with a simple, secure single sign-on (SSO) solution for today's education applications.  By integrating with Clever, you'll get students and teachers using your app in a jiffy.

Use **Clever Instant Login** for the following core use cases:

1. **Sign users in from district portals** - Students and teachers can sign in to your web application from Clever
2. **Log in with Clever** - Students and teachers can sign in to your app using Clever

For additional use cases, see: [About Clever Instant Login](https://dev.clever.com/instant-login/).

To get started, we'll be providing you a general overview of **Use Case #1** and a sample implementation using a basic Python [Flask](http://flask.pocoo.org/) app.

### Scenario
A district admin is using the Clever portal to manage various education apps for schools, students, and teachers in her district.  From the Clever portal, she sees an icon to your app, and we'd like to give her the ability to sign right -- without fumbling over usernames and passwords. 

This Flask implementation will handle the redirect from Clever, determine the user id, and display the first and last name of the user.

# Getting Started
### Requirements
Whether you'd like to integrate today or play around with the sample Flask app, you'll need a few things in place first.

1. Go to https://apps.clever.com/signup to register your app with Clever.
2. Configure the **OAuth Settings** for your app in the [Clever App Dashboard](https://account.clever.com/partner/applications).
3. Configure your [Sandbox District](https://dev.clever.com/guides/creating-district-sandboxes) to build and test your integration.

After these steps are completed, you are ready to start checking out the Clever APIs.

### Signing users in from district portals
Clever provides school districts with a customizable portal that gives students and teachers a centralized place to manage their apps.  To enable users to sign in from district portals, you will be implementing a simplified [OAuth 2.0](http://oauth.net/2/) credential acquisition flow.

**1. Clever will redirect users to your web application**

Your web application will handle an `HTTP` `GET` request from the authenticated user from the district Clever portal.  Clever redirects to your site with a temporary code in a `code` parameter.

The Clever **Instant Login Link** for your app contains a `client_id` of your app and the `district_id` of the user, like this: 

``https://clever.com/oauth/instant-login?client_id=123450dc123c8d841645&district_id=675cadfe740eed01000004d6``

When a user clicks on the **Instant Login Link**, Clever redirects the user to your app, like this:

`GET` ``<redirect_uri>?code=12345b6d8fc464ab8242b89de623c0696ca02b1e&scope=read%3Astudents%20read%3Adistrict_admins%20read%3Aschool_admins%20read%3Auser_id%20read%3Ateachers``

**Note**: For security reasons, the `code` generated for the user is no longer valid after it has been used to exchange for an access token and can expire before it is exchanged for an access token.

**Parameters**

| Field | Type | Description |
|-----------|-------------|-------------------|
| `redirect_uri` | `string` | The URL for your application where users will be sent from the Clever portal and can be configured in Clever Developer Dashboard settings (i.e. ``http://localhost:5000/oauth``)|
| `code` | `string` | The code received Clever is used to exchange for the user's access token |
| `scope` | `string` | A space-delimited, urlencoded list of [scopes](https://dev.clever.com/instant-login/implementation#scopes). Defaults to an empty list for users who have not authorized any scopes for the application. |

From the sample Flask app, our application entry-point (*app.py*) contains a route that handles the incoming request like so:
```python
@app.route('/oauth', methods=['GET'])
def oauth():
    name = server.oauth(request)
    return render_template('results.html', name=name)
```
Server-side logic will be found in *server.py*.

**2. Exchange code for an access token**

Create a [`Basic Authentication`](https://tools.ietf.org/html/rfc6749) header using `CLIENT_ID` and `CLIENT_SECRET`.

``Authorization: <type> <credentials>``

**Parameters**

| Field | Description |
|------|-------------|
| `type` |  HTTP authentication scheme type (e.g.`Basic`) |
| `credentials` | Base64 result of string "`CLIENT_ID`:`CLIENT_SECRET`"|
|`CLIENT_ID` | The client ID you received from Clever when you registered your app |
|`CLIENT_SECRET` | The client secret you received from Clever when you registered your app |

From our sample Flask app, *server.py*, we use the Python [`base64`](https://pymotw.com/2/base64/) module:
```python
    headers = {
        'Authorization': 'Basic {base64string}'.format(
            base64string=base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)),
        'Content-Type': 'application/json'
    }
```
Use this header to make the following API request to Clever and get the access token for the user:

``POST https://clever.com/oauth/tokens``

**Parameters**

| Field | Description |
|-------|-------------|
| `code` | The code received from Clever and is used to exchange for the user's access token |
| `grant_type` | OAuth 2.0 grant type. (e.g. `authorization_code`)|
| `redirect_uri` | The URL for your application where users will be sent from the Clever portal and can be configured in Clever Developer Dashboard settings (i.e. ``http://localhost:5000/oauth``) |

**Sample Request**
```
POST https://clever.com/oauth/tokens
Authorization: Basic YW5WcFkyVnFkV2xqWldwMWFXTmxDZzpjY1hwWTR0cWRZbGVjNHAxYUdsMXVJ
Content-type: application/json
Content-length: 113
{"code":"12345b6d8fc464ab8242b89de623c0696ca02b1e","grant_type":"authorization_code","redirect_uri":"http://localhost.com:5000/oauth"}`
```

**Sample Response**
```
TODO
```
**Note**: If you have successfully completed this step, you have obtained the bearer token for the user. Bearer tokens are used in HTTP requests to access OAuth 2.0 protected resources. Any party in possession of a bearer token (a "bearer") can use it to get access to the associated resources.  You should ensure that your app is securely saving and using bearer tokens to prevent misuse of the Clever APIs.

**3. Use the access token to access the API**

Create a [`Bearer`](https://tools.ietf.org/html/rfc6749) header using the bearer token.

``Authorization: <type> <credentials>``

**Parameters**

| Field | Description |
|------|-------------|
| `type` |  HTTP authentication scheme type (e.g.`Bearer`) |
| `credentials` | Access token retrieved for the user in Step 2. |

From our sample server.py:
```python
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
```
You will need use header when making API requests on behalf of the authenticated user.

### Using the Identity API
Using the Bearer header and the bearer token for the user, you can also now use the Clever Data API to learn more about the user.

`GET` `https://api.clever.com/me`

**Response**

| Field | Description|
|--------|------------|
| id | A unique user `id` is required for requests from the Clever [Data API](https://clever.com/developers/docs/explorer#api_data) set
| type | Clever [user type]((https://dev.clever.com/instant-login/users)) (i.e. `district_admin`)|
|district | `district_id` of the user |

**Sample request**

`GET` `https://api.clever.com/district_admins/{id}`

**Sample response**
```
TODO
```

# Demo
### Installation
If you'd like to contribute to the project or try an unreleased version of the sample Flask app locally, run the following commands in your terminal:


```bash
# clone the repository
git clone git@github.com:emmma/clever.git

cd clever

# install dependencies
pip install -r requirements.txt

#set up required environment variables for Flask.
export FLASK_APP=app.py

# (optional) enable debugging for the app
export FLASK_DEBUG=1
```

Set up `CLIENT_ID` and `CLIENT_SECRET` for your local machine.  Replace the `<value>` with the exact value that is found in the **OAuth Settings** for your app.

```bash
export CLIENT_ID='<value>'
export CLIENT_SECRET='<value>' 
```
### Usage
To run the app, type the following command in your terminal:
```bash
flask run
```
This will launch the app on your machine.  Flask will also log debugging information in the terminal.  You should see a response similar to the following below:
>> Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

You can go to a web browser of your choice and type in the URL provided (e.g. http://127.0.0.1:5000/) to interact with the app.

## Additional Resources
#### Clever
* [About Clever Instant Login](https://dev.clever.com/instant-login/)
* [Implementing Clever SSO](https://dev.clever.com/instant-login/implementation)
* [Log in with Clever](https://dev.clever.com/instant-login/log-in-with-clever)
* [Testing Your Integration](https://dev.clever.com/instant-login/testing)
#### Flask
* [Flask](http://flask.pocoo.org/)
* [Application Errors](http://flask.pocoo.org/docs/0.11/errorhandling/)

#### Extraneous
* [HTTP Status and Error Codes](https://cloud.google.com/storage/docs/json_api/v1/status-codes)
* [Python `requests.status codes`](https://github.com/kennethreitz/requests/blob/master/requests/status_codes.py)

## TODO
Do you see ways to improve the demo app for new devs like yourself on the Clever platform?  If you see ways to improve the demo app, feel free to contribute to the project!


* Optimize error handling for retry() for HTTP 4XX and HTTP 5XX errors
* Set up better logging for errors and exceptions
* Set up automated tests
* Make additional calls to the Clever Data API

# Contact Us 
Questions, feature requests, or feedback of any kind is always welcome! We'd love to hear from you at tech-support@clever.com.  Empower students and teachers today.  *Do it the Clever way.*
