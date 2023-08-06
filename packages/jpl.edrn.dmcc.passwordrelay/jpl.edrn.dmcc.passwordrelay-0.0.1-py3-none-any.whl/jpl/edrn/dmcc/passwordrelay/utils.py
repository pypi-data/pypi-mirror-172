# encoding: utf-8

'''🏃 Utilities.

You can invoke this module with ``python -m`` passing in a username and password to test with
the default ``DMCC_SOAP_URL``.
'''

from .constants import DMCC_SOAP_URL, DIM_VALIDATION_TOKEN
from zeep import Client
from zeep.cache import InMemoryCache
from zeep.transports import Transport
import logging, argparse, enum, sys

_logger = logging.getLogger(__name__)
_transport = Transport(InMemoryCache())


class PasswordStatus(enum.Enum):
    '''An enumeration describing the three states of DMCC password validation.'''
    VALID = 'valid'
    INVALID = 'invalid'
    EXPIRED = 'expired'


def add_logging_arguments(parser: argparse.ArgumentParser):
    '''Add our usual command-line logging options.'''
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--debug', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO,
        help='🐞 Log copious and verbose messages suitable for developers'
    )
    group.add_argument(
        '--quiet', action='store_const', dest='loglevel', const=logging.WARNING,
        help="🤫 Don't log informational messages"
    )


def validate_password(username: str, password: str) -> PasswordStatus:
    '''Check if the ``username`` is credentialed by the ``password`` against the DMCC SOAP service.'''
    _logger.debug('Creating SOAP client to %s', DMCC_SOAP_URL)
    client = Client(DMCC_SOAP_URL, transport=_transport)
    _logger.debug('Calling ``pwdVerification`` with username %s', username)
    response = client.service.pwdVerification(username, password, DIM_VALIDATION_TOKEN)
    if response == 'valid':
        _logger.debug('Password for %s is valid', username)
        return PasswordStatus.VALID
    elif response == 'expired':
        _logger.debug('Password for %s expired', username)
        return PasswordStatus.EXPIRED
    else:
        _logger.debug('Password for %s is invalid', username)
        return PasswordStatus.INVALID


if __name__ == '__main__':
    print(validate_password(sys.argv[1], sys.argv[2]))
