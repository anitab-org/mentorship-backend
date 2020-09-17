# Integrating third part authentication
Task: To design a probable solution for integrating third-party apps authentication. So that end-user can log in from other social media platforms and third-party apps.

## Overview
The current approach for User Authentication is JSON Web Token (JWT) based using a flask extension (flask-jwt-extended) using an authentication token. 

## Contents
* OAuth
* Auth0 Implementation
* Local Setup
* Third-Party Authentication: Auth0
* Other Possible Solutions
* References

## OAuth
OAuth provides a way to authorize and revoke access to your account to yourself and third parties.
Third parties can use this to provide services, such as monitoring and scaling your applications. You can also use these tokens obtained with OAuth to grant access for your own scripts on your machine or to other applications.

### Using OAuth on Heruku Platform
* The Heroku Platform API implements OAuth version 2.0 as the preferred authentication mechanism.

## Auth0
Auth0 is an add-on for providing single sign on and user management with social and enterprise identities.
* Enable Email/Password authentication and Single Sign On with brute force protection for all your apps (web, single page, native or hybrid).
* Consolidate/migrate your own user repositories (PG, mySql, SQL Server, Mongo, etc.) under a single identity store as they login (no bulk import needed)
* Add SAML authentication without worrying about the integration with multiple providers (ADFS, SiteMinder, PingFederate, Okta, OneLogin, etc.), we take care of that.
* Add social authentication with Google, Facebook, Microsoft Account, 30+ others or any other OAuth2 provider.
* Get a normalized user profile regardless of the provider used.
* Add support for linking user accounts manually or automatically by email.
* Pull data from other sources and add it to the user profile, through JavaScript rules.
* Single Sign On with Third Party Apps/Platforms like WordPress, Zendesk, Drupal, and more.
* Auth0 is accessible via an API and has supported client libraries for Ruby, Node.js and many others. 

### Provisioning the add-on
List of plans are available [here](https://elements.heroku.com/addons/auth0)

```sh
$ heroku addons:create auth0 --type=[nodejs|rails] --subdomain=myapp
-----> Adding Auth0 to sharp-mountain-4005... done, v18 (free)
```
Once Auth0 has been added you will have three settings on your app:

* AUTH0_CLIENT_ID: the id that identifies your application.
* AUTH0_CLIENT_SECRET: the secret for your application
* AUTH0_DOMAIN: you will get your own subdomain on auth0
* AUTH0_CALLBACK_URL: the url where auth0 will redirect the user after authentication
```sh
heroku config:get AUTH0_CLIENT_ID
9jf020kksfiuhifruiudtgudjsoeiuk
```
After installing Auth0 the application should be configured to fully integrate with the add-on.

## Local Setup
### Environment Set-Up
After provisioning the add-on it’s necessary to locally replicate the config vars so your development environment can operate against the service.
* Though less portable it’s also possible to set local environment variables using export AUTH0_CLIENT_ID=value.

Use the Heroku Local command-line tool to configure, run and manage process types specified in your app’s Procfile.
Heroku Local reads configuration variables from a .env file. 
To view all of your app’s config vars, type heroku config. 
Use the following command to add the values retrieved from heroku config to your .env file.

## Third-Party Authentication: Auth0
1. Update your application's ownership to third-party in Auth0.
2. By default, applications registered in Auth0 are first-party applications. If you want your application to be a third-party application, you must update its ownership.
3. Promote the connections you will use with third-party applications to domain level in Auth0.
4. Third-party applications can only authenticate users from connections flagged as domain-level connections. Domain-level connections can be enabled for selected first-party applications while also being open to all third-party application users for authentication.
5. Update your application's login page. If you use Lock in the Universal Login Page, you must also: sh Upgrade to Lock version 11 or later. 
6. Set the __useTenantInfo: config.isThirdPartyClient flag when instantiating Lock.
For Private Cloud users only: Set the configurationBaseUrl option to https://{config.auth0Domain}/ when instantiating Lock.

Neither first- nor third-party applications can use ID tokens to invoke Management API endpoints. 
Instead, they should get access tokens with the following ```sh current_user_* ``` scopes required by each endpoint.

### Script Example
```sh
<script src="https://cdn.auth0.com/js/lock/11.x.y/lock.min.js"></script>
...
<script>
  // Decode utf8 characters properly
  var config = JSON.parse(decodeURIComponent(escape(window.atob('@@config@@'))));
  var connection = config.connection;
  var prompt = config.prompt;
  var languageDictionary;
  var language;
  if (config.dict && config.dict.signin && config.dict.signin.title) {
    languageDictionary = { title: config.dict.signin.title };
  } else if (typeof config.dict === 'string') {
    language = config.dict;
  }
  var lock = new Auth0Lock(config.clientID, config.auth0Domain, {
    auth: {
      redirectUrl: config.callbackURL,
      responseType: config.callbackOnLocationHash ? 'token' : 'code',
      params: config.internalOptions
    },
    assetsUrl:  config.assetsUrl,
    allowedConnections: connection ? [connection] : null,
    configurationBaseUrl: 'https://' + config.auth0Domain + '/', // for PSaaS only
    rememberLastLogin: !prompt,
    language: language,
    languageDictionary: languageDictionary,
    closable: false,
    __useTenantInfo: config.isThirdPartyClient // required for all Tenants
  });
  lock.show();
</script>
```
## Other Solutions
### Azure App Service
[Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/overview-authentication-authorization) provides built-in authentication and authorization support, so you can sign in users and access data by writing minimal or no code in your web app, RESTful API, and mobile back end, and also Azure Functions.
#### Following are some applications of this service and links to configure azure services for authentication using them:
* [Facebook login](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-facebook)
* [Microsoft account login](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-microsoft)
* [Twitter login](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-twitter)
* [Google login](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-google)
### Oneall Social Login
[Social Login](https://www.oneall.com/services/social-network-integration/social-login/) allows your users to login and register with one click on your website or mobile application using their existing accounts from 40+ Social Networks. 
Improve your sign-up rate, obtain pre-validated email addresses and gather rich demographic data about your users without using any forms.
* Add Social Login to your website by embedding a few lines of JavaScript or use our Direct Connect service for a javascriptless implementation on mobile devices.
* Social Login is fully customizable and supports hooks and events that can be triggered whenever a user logs in. 
* A full implementation guide and a JSON/REST API complete the offered service.
#### Code Example
```sh
<div id="social-login-container"></div>
<script type="text/javascript">
    var _oneall = _oneall || [];
    _oneall.push(
        ['social_login', 'set_providers', ['facebook', 'twitter', 'pinterest', 'dribbble', 'google', 'steam', 'vimeo', 'twitch']],
        ['social_login', 'set_callback_uri', window.location.href],
        ['social_login', 'set_custom_css_uri', 'https://secure.oneallcdn.com/css/api/themes/flat_w188_h32_wc_v1.css'],
        ['social_login', 'do_render_ui', 'social-login-container']
    );
</script>
```
## References
* [Heroku Dev Center](https://devcenter.heroku.com/articles/auth0)
* [Auth0 Docs for third party authentication](https://auth0.com/docs/applications/enable-third-party-applications)
* [Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/overview-authentication-authorization)
