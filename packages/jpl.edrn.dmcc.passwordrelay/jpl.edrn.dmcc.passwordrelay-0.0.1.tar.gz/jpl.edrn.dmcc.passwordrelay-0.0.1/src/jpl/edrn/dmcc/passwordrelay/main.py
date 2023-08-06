# encoding: utf-8

'''🏃 EDRN DMCC Password Relay: main entrypoint.'''


from . import VERSION
from .constants import DEFAULT_SOCKET
from .server import PasswordVerificationHandler
from .utils import add_logging_arguments
import os, argparse, logging, socketserver

_logger = logging.getLogger(__name__)
__version__ = VERSION


def main():
    '''Entrypoint: parse args, start the server, and wait.'''
    parser = argparse.ArgumentParser(description='EDRN DMCC Password Relay')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    add_logging_arguments(parser)
    parser.add_argument(
        '-s', '--socket', default=DEFAULT_SOCKET,
        help='🔌 Path to the Unix domain socket to create (will be deleted if it already exists) [%(default)s]'
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s %(message)s')
    socket_path = args.socket
    _logger.debug('Using socket at %s', socket_path)
    if os.path.exists(socket_path):
        _logger.debug('Socket already exists at %s; deleting it', socket_path)
        os.unlink(socket_path)
    os.makedirs(os.path.dirname(socket_path), exist_ok=True)
    _logger.info('Starting DMCC Relay Server listening on %s', socket_path)
    with socketserver.UnixStreamServer(socket_path, PasswordVerificationHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
