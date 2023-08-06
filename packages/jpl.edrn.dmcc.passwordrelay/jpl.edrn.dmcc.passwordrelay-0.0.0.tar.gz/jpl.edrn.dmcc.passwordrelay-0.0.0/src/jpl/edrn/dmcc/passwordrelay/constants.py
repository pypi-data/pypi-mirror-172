# encoding: utf-8

'''🏃 DMCC Password Relay: constants.'''


# Where the DMCC SOAP service lives
DMCC_SOAP_URL = 'https://www.compass.fhcrc.org/edrn_ws/ws_newcompass.asmx?WSDL'

# Where to create our listening socket by default
DEFAULT_SOCKET = '/tmp/dmcc.socket'

# The vapid validation token that serves no purpose
DIM_VALIDATION_TOKEN = '0' * 4096
