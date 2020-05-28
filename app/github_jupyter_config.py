from oauthenticator.github import LocalGitHubOAuthenticator
c.JupyterHub.authenticator_class = LocalGitHubOAuthenticator

c.LocalGitHubOAuthenticator.create_system_users = True

## Add the administrator(s) to this list
#c.Authenticator.admin_users = {'chbrandt'}

## Add allowed users to this list if you want to restrict access
#c.Authenticator.whitelist = {'joao','maria'}

import os
c.LocalGitHubOAuthenticator.client_id = os.environ['GITHUB_CLIENT_ID']
c.LocalGitHubOAuthenticator.client_secret = os.environ['GITHUB_CLIENT_SECRET']
c.LocalGitHubOAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'
