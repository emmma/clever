# Supporting Clever Instant Login in Flask
The Clever platform provides school districts everywhere with a simple, secure single sign-on (SSO) solution for a variety of student and teacher applications.  Developers like yourself can leverage Clever to spare students and teachers the pain of maintaining disparate identity systems for their daily apps.  

Clever provides schools with a portal to centralize their application management experience.  For developers, Clever provides an easy way for you to integrate and showcase your app in the customizable Clever portal for school districts, giving students and teachers easy access to your app.

**Clever Instant Login** supports the following core use cases:
1. Users can [sign in to your web application from the district Clever portal(s)](https://dev.clever.com/instant-login/bearer-tokens)
2. Users can [sign in to district Clever portals from your web application](https://dev.clever.com/instant-login/log-in-with-clever)

For additional use cases, please see [About Clever Instant Login](https://dev.clever.com/instant-login/).  For the purposes of this exercise, we will be providing an overview of the integration and a sample Flask app that demonstrates both functionalities.

## 1. Signing users in from district portals
To enable users to sign in from district portals, you will be implementing a simplified [OAuth 2.0](http://oauth.net/2/) credential acquisition flow.

Your web application will handle an `HTTP` `GET` request from the authenticated user of the district Clever portals.  The request will contain a `code` parameter and a `scope` parameter in the URI.  You will use the `code` value to exchange for the user's Clever access token to complete the OAuth dance.

### Obtaining Bearer Tokens
Please ensure that your app is first configured correctly in your [Clever App Dashboard](https://account.clever.com/partner/applications).  In particular, you will need the information configured in the **OAuth Settings** for your app.

Your **Redirect URLS** must be registered in the settings for Clever to send the `HTTP` `GET` request to your web application.  To enable Clever Instant Login, make sure that at least one checkbox for **Students**, **Teachers**, **School Admins**, and **District Admins** is selected.  The **Client ID** is unique to your app and the corresponding **Client Secret** should never be shared.

### Calling the "/me" API
After you have successfully retrieved the user's access token from Clever, you can start making API requests for the user's behalf.  To begin, you will use the *bearer token* for the user when making an API call.

To determine the user, you can get the user `id` from the `GET` `https://api.clever.com/me` endpoint.  This user `id` uniquely identifies the user in the system and is required for requests from the Clever [Data API](https://clever.com/developers/docs/explorer#api_data) set.

The sample Flask app will call the `/me` endpoint to retrieve the user `id` and user `type`.  Based on the user `type`, the app will make an additional API call (e.g. `/students/{id}`) to get specific user information, such as the `name` object.

To learn more about supported user types, see [Working with Clever Users](https://dev.clever.com/instant-login/users).

## 2. Signing users in with Log in with Clever
TODO

# Demo
The sample Flask app demonstrates a basic integration with **Clever Instant Login**.
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
Questions, feature requests, or feedback of any kind is always welcome! We'd love to hear from you at tech-support@clever.com.  

Empower students and teachers today.  *Do it the Clever way.*