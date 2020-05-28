# Log in JupyterHub through UltraAuth facial/biometric authentication system

UltraAuth provides an OpenID iterface to authenticate users in its biometric database.
So the idea here is to workout the OAuth client interface provided by JupyterHub
to authenticate through UltraAuth.

In case you have experience on setting up an App to authenticate using GitHub' OAuth
interface, the process on UltraAuth' OpenID is very similar, we just have to give
a bit more of information.

In general, the process is (i) deploy your App (either locally or on the cloud),
(ii) create an entry for your App in UltraAuth, (iii) set UltraAuth' OpenID endpoints
and tokens on your (local) App.


## Deploy (local) App

Our _App_ here is _JupyterHub_.
JupyterHub provides a generic client interface of OAuth authentication system,
which is sufficient to our goals since OpenID is based on OAuth-2.

First step then is to have a working _JupyterHub_ environment with Python
`oauthenticator` library installed.
To that, you can simply use `pip` to have `jupyterhub`, `notebook`, `oautheticator`
packages installed.

By now, JupyterHub should be ready to run.
By default, JupyterHub runs on port `8000`; if that's OK to you, go ahead:
```bash
# jupyterhub
```

Opening your browser at address `http://localhost:8000` should bring JupyterHub's
login interface.
That being the case, good: hereafter, our App URL is `http://localhost:8000`.
We may now -- for the next step -- shutdown our JupyterHub service.


## Create UltraAuth App

Now it is time to create an entry for our App (JupyterHub) in UltraAuth.
Once we login to UltraAuth we may go to the Apps section, and create a
[New Application](https://www.ultraauth.com/apps/new).

Fill the following fields as follows:
* `Website / Domain URL`: `http://localhost:8000`
* `Application Type`: `Web`
* `Token Endpoint`: `client_secret_basic`
* `Callback URI`: `http://localhost:8000/hub/oauth_callback`
* `Logout URI`: `http://localhost:8000/logout`

Then hit the button to Create/Update App.
A new page will come out with your `CLIENT_ID` and `CLIENT_SECRET` tokens,
those values are uniquely generated to each user/app and should be kept safe.


## Config our JupyterHub App to UltraAuth servers

Now that we have our tokens we may go back to our JupyterHub and set it accordingly.

JupyterHub app provides a `-f` option to pass a (`jupyterhub`) config file,
which in our case is as simple as:

[`jupyterhub_config.py`]
```python
c.JupyterHub.authenticator_class = 'oauthenticator.generic.GenericOAuthenticator'
```

Here we are simply declaring that the authentication system to be used by
JupyterHub will be provided by OAuthenticator's `GenericOAuthenticator`
[1](https://github.com/jupyterhub/oauthenticator/blob/master/oauthenticator/generic.py).
By default, this class reads parameters from the environment around.
To our use case the following environment variables should be defined:

[`ultraauth.env`]
```bash
export OAUTH_CLIENT_ID="$ULTRAAUTH_CLIENT_ID"
export OAUTH_CLIENT_SECRET="$ULTRAAUTH_CLIENT_SECRET"

export OAUTH_CALLBACK_URL='http://localhost:8000/hub/oauth_callback'

export OAUTH2_AUTHORIZE_URL="https://srv.qryp.to/op/auth?scope=openid email address profile"
export OAUTH2_TOKEN_URL='https://srv.qryp.to/op/token'
export OAUTH2_USERDATA_URL='https://srv.qryp.to/op/me'
```

Where `ULTRAAUTH_CLIENT_ID` and `ULTRAAUTH_CLIENT_SECRET` are the tokens we got
from UltraAuth when we created our App entry.
The endpoints server `https://srv.qryp.to` can be taken from the sample apps in
UltraAuth (_e.g_, [Django OpenID UltraAuth Connect](https://elements.heroku.com/buttons/deauthorized/python_openidconnect_starter_app))

Once those Environment Variables are declared, we may run again `jupyterhub` giving
now the config file above:
```bash
# jupyterhub -f jupytherhub_config.py
```

We may now open a new browser window at `http://localhost:8000` and a new login
dialog providing a simple button "Sign in with GenericOauth2".
Click it, and you should now get the biometric validation methods provided
by UltraAuth as explained in its introductory video at https://www.ultraauth.com/select-strategy.


## Conclusion

We have presented a direct, easy way to integrate a JupyterHub instance to
biometric-based authentication provided by UltraAuth.
