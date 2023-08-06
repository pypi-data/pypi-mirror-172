# encoding: utf-8

'''🏃 DMCC Password Relay: server-side handling.'''

from .utils import validate_password, PasswordStatus
import socketserver, logging

_logger = logging.getLogger(__name__)


class PasswordVerificationHandler(socketserver.StreamRequestHandler):
    '''Handler for stream requests to verify a username and a password. Sends back a single octet of
    061 for valid passwords, 060 for anything else. We don't differentiate between expired and invalid.
    '''
    def handle(self):
        uid, password = self.rfile.readline().decode('utf-8').strip(), self.rfile.readline().decode('utf-8').strip()
        # User IDs are full LDAP Distinguished Names (DNs) of the form
        #     uid=USERNAME,dc=edrn,dc=jpl,dc=nasa,dc=gov
        # so strip off all but the USERNAME
        uid = uid[4:uid.index(',')]
        status = validate_password(uid, password)
        rc = 1 if status == PasswordStatus.VALID else 0
        _logger.info('For username %s the password was %s so sending back %d', uid, status, rc)
        self.wfile.write(f'{rc}'.encode('utf-8'))
