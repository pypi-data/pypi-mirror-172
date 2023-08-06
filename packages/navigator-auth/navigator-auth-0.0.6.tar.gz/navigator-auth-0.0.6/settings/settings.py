from navconfig import config
from navigator_auth.conf import * # pylint: disable=W0401

AUTH_MISSING_ACCOUNT = config.get(
    'AUTH_MISSING_ACCOUNT', fallback='create'
)

# List of function callbacks called (in order) when a user is
AUTH_SUCCESSFUL_CALLBACKS = (
    # 'resources.auth.last_login',
    # 'resources.auth.saving_troc_user'
)

AUTHORIZATION_MIDDLEWARES = (
    # 'navigator.auth.middlewares.django_middleware',
    # 'navigator.auth.middlewares.troctoken_middleware',
)

AUTHENTICATION_BACKENDS = (
 #'navigator.auth.backends.TrocToken',
 #'navigator.auth.backends.TokenAuth',
 #'navigator.auth.backends.GoogleAuth',
 # 'navigator.auth.backends.OktaAuth',
 #'navigator.auth.backends.ADFSAuth',
 # 'navigator.auth.backends.AzureAuth',
 #'navigator.auth.backends.GithubAuth',
 'navigator_auth.backends.BasicAuth',
 'navigator_auth.backends.DjangoAuth',
 'navigator_auth.backends.NoAuth',
)
