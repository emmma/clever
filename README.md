# Supporting Clever Instant Login in Flask
[Clever APIs](https://dev.clever.com/) empower developers and school districts everywhere with a simple, secure single sign-on (SSO) solution for today's education applications.  By integrating with Clever, you'll get students and teachers using your app in a jiffy.

Use **Clever Instant Login** for the following core use cases:
1. **Sign users in from district portals** - Students and teachers can [sign in to your web application from Clever](https://dev.clever.com/instant-login/bearer-tokens).
2. **Log in with Clever** - Students and teachers can [sign in to Clever from your web application](https://dev.clever.com/instant-login/log-in-with-clever).

For additional use cases, see: [About Clever Instant Login](https://dev.clever.com/instant-login/).

To give you a better idea of how this integration would work with your application, we'll give you an overview to get you started, along with a basic, barebone [Flask](http://flask.pocoo.org/) (Python) app that incorporates the **Clever Instant Login** core use cases.

# Web Application Flow
### Requirements
1. Go to https://apps.clever.com/signup to register your app with Clever.
2. Configure the **OAuth Settings** for your app in the [Clever App Dashboard](https://account.clever.com/partner/applications).
3. Configure your [Sandbox District](https://dev.clever.com/guides/creating-district-sandboxes) to build and test your integration.

### Signing users in from district portals
Clever provides school districts with a customizable portal that gives students and teachers a centralized place to manage their apps.  To enable users to sign in from district portals, you will be implementing a simplified [OAuth 2.0](http://oauth.net/2/) credential acquisition flow.

**1. Clever will redirect users to your web application**

Your web application will handle an `HTTP` `GET` request from the authenticated user from the district Clever portal.  Clever redirects to your site with a temporary code in a `code` parameter.

In the Clever district portal, Clever provides an **Instant Login Link** for your app and your users, containing the `client_id` of your app and the `district_id` of the user, like this: 

``https://clever.com/oauth/instant-login?client_id=123450dc123c8d841645&district_id=675cadfe740eed01000004d6``

When a user goes to that URL, Clever will resolve the **Instant Login Link** to the effective `GET` request to your app, like this:

`GET` ``<redirect_uri>?code=12345b6d8fc464ab8242b89de623c0696ca02b1e&scope=read%3Astudents%20read%3Adistrict_admins%20read%3Aschool_admins%20read%3Auser_id%20read%3Ateachers``

**Note**: For security reasons, the `code` generated for the user is no longer valid after it has been used to exchange for an access token and can expire before it is exchanged for an access token.

**Parameters**
| Field | Type | Description |
|-----------|-------------|-------------------|
| `redirect_uri` | `string` | The URL for your application where users will be sent from the Clever portal and can be configured in Clever Developer Dashboard settings (i.e. ``http://localhost:5000/oauth``)|
| `code` | `string` | The code received Clever is used to exchange for the user's access token |
| `scope` | `string` | A space-delimited, urlencoded list of [scopes](https://dev.clever.com/instant-login/implementation#scopes). Defaults to an empty list for users who have not authorized any scopes for the application. |

In our sample Flask app, *app.py* has a route */oauth* where the application expects the incoming `GET` request from Clever like so:
```python
@app.route('/oauth', methods=['GET'])
def oauth():
    return server.incoming(request)
```
*server.py* contains the server-side logic for the next steps.

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

In our sample Flask app, *server.py*, we use the Python [`base64`](https://pymotw.com/2/base64/) module:
```python
    headers = {
        'Authorization': 'Basic {base64string}'.format(base64string = base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)),
        'Content-Type': 'application/json'
    }
```
Use the header to make the following API request to Clever:

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

In our sample Flask app, server.py:
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

**Sample response**

`GET` `https://api.clever.com/district_admins/{id}`

## 2. Signing users in with Log in with Clever
TODO

# Demo
### Installation
If you'd like to contribute to the project or try an unreleased version of the sample Flask app locally, run the following commands in your terminal:


```bash
# clone the repository
git clone git@github.com:emmolam/clever.git
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
* [About Clever Instant Login](https://dev.clever.com/instant-login/)
* [Implementing Clever SSO](https://dev.clever.com/instant-login/implementation)
* [Log in with Clever](https://dev.clever.com/instant-login/log-in-with-clever)
* [Testing Your Integration](https://dev.clever.com/instant-login/testing)
* [Flask](http://flask.pocoo.org/)

# Contact Us 
Questions, feature requests, or feedback of any kind is always welcome! We'd love to hear from you at tech-support@clever.com.  Empower students and teachers today.  *Do it the Clever way.*