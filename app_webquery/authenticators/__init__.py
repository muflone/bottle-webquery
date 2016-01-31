import logging

from .dummy import AuthenticatorDummy

ALGORITHMS_CLASSES = {
  AuthenticatorDummy.ALGORITHM: AuthenticatorDummy,
}
KEY_USERNAME = 'username'
KEY_FULLNAME = 'fullname'
KEY_ROLES = 'roles'

def check_login(db_settings, username, password):
  result = db_settings.get_data(
    'SELECT description, algorithm, roles '
    'FROM users '
    'WHERE name=?',
    None,
    (username, ))[1]
  if result:
    description, algorithm, roles = result[0]
    if algorithm in ALGORITHMS_CLASSES:
      authenticator = ALGORITHMS_CLASSES[algorithm](db_settings)
      if authenticator.check_login(username, password):
        return {
          KEY_USERNAME: username,
          KEY_FULLNAME: description,
          KEY_ROLES: roles.split(',')
        }
    else:
      logging.error('unexpected algorithm "%s"' % algorithm)
  return None
