from . import Message_pb2
from socket import socket, AF_INET
from ssl import wrap_socket
from struct import pack, unpack
from zlib import decompress, compress
import hashlib
import platform
import subprocess


def unpack_data(packet):
    """
    Unpack the data from a binary packet, possibly decompressing if gzip-compressed.

    Args:
        packet (bytes): The binary packet containing the header and data.

    Returns:
        bytes: The unpacked data.

    The unpack_data function extracts the data from a binary packet. The packet is expected
    to have a header containing the length of the data and a flag indicating whether gzip
    compression was used. The function first unpacks the header to retrieve the data length
    and the compression flag. If the compression flag is set to 2, indicating gzip compression,
    the data is decompressed using gzip.

    Parameters:
        packet (bytes): The binary packet containing the header and data.

    Returns:
        bytes: The unpacked data.

    Example:
        received_packet = b'\x00\x00\x00\x1c\x00\x00\x00\x02This is compressed data...'
        data = unpack_data(received_packet)
        # The extracted data can be further processed and used as needed.
    """
    header = unpack('>ibbbb', packet[:8])
    data = packet[8:]
    if header[1] == 2:
        data = decompress(data, -15)
    return data


def pack_data(data, gzip=False):
    """
    Pack the given data into a binary packet with an optional gzip compression.

    Args:
        data (bytes): The raw data to be included in the packet.
        gzip (bool, optional): If True, the data will be compressed using gzip compression.
                               Defaults to False.

    Returns:
        bytes: The binary packet containing the header and (optionally compressed) data.

    The pack_data function constructs a binary packet with the provided data and an optional
    gzip compression. The data is first optionally compressed using gzip, and then a header is
    built for the packet. The header includes the length of the data and a flag indicating
    whether gzip compression is used.

    Parameters:
        - data (bytes): The raw data to be included in the packet.
        - gzip (bool, optional): If True, the data will be compressed using gzip compression.
                                 Defaults to False.

    Returns:
        bytes: The binary packet containing the header and (optionally compressed) data.

    Example:
        raw_data = b'This is the raw data that needs to be packed.'
        packet = pack_data(raw_data, gzip=True)
        # The resulting packet can be transmitted or stored as needed.
    """
    if gzip:
        data = compress(data, wbits=-15)
    header = pack('>ibbbb', len(data), 2 if gzip else 0, 0, 0, 0)
    packet = header + data
    return packet


def get_gps(state):
    """
    Extracts and processes GPS data from the provided state object.

    This function reads the state object, which is assumed to have a specific structure.
    It then calculates latitude and longitude in degrees from the state object's raw GPS data,
    which is assumed to be given in degrees and minutes.

    If the GPS switch is not enabled in the state object, the function will return 0 for both latitude and longitude.

    Parameters:
    state (object): An object that contains GPS data. The structure of this object is assumed to be as follows:
                    - state.gps.gpsSwitch.enabled: A boolean indicating if the GPS is enabled.
                    - state.gps.gpsPos.gpsLat: A string representing the latitude data in degrees and minutes.
                    - state.gps.gpsPos.gpsLong: A string representing the longitude data in degrees and minutes.

    Returns:
    dict: A dictionary with the following keys:
          - 'enabled': A boolean indicating whether the GPS was enabled.
          - 'latitude': The latitude in degrees. It's negative, as values are assumed to be in the southern hemisphere.
          - 'longitude': The longitude in degrees.
    """
    if state.gps.gpsSwitch.enabled:
        # get degrees
        lat_deg = float(state.gps.gpsPos.gpsLat[0:2])
        lon_deg = float(state.gps.gpsPos.gpsLong[0:3])
        # get minutes
        lat_min = float(state.gps.gpsPos.gpsLat[2:9])
        lon_min = float(state.gps.gpsPos.gpsLong[3:10])
        # create dictionary to return
        return {
            'enabled': True,
            'latitude': -1 * (lat_deg + (lat_min / 60)),
            'longitude': lon_deg + (lon_min / 60)
        }
    else:
        return {
            'enabled': False,
            'latitude': 0,
            'longitude': 0
        }


def is_host_reachable(host):
    """
   Checks if a host is reachable by sending a single ICMP echo request ("ping") to the host.

   This function constructs the appropriate ping command depending on the operating system
   (either Windows or a UNIX-like system such as Linux or MacOS), then attempts to execute the command.
   The host is considered reachable if the return code of the ping command is 0 (which means the command
   was successful).

   Parameters:
   host (str): The hostname or IP address of the target host.

   Returns:
   bool: True if the host is reachable (the ping command was successful), False otherwise.
   """
    # Determine the appropriate ping command based on the operating system.
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", host]
    else:
        cmd = ["ping", "-c", "1", host]

    try:
        # Run the ping command and check the return code.
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return True  # If the return code is 0, the host is reachable.
    except subprocess.CalledProcessError:
        return False  # If the return code is non-zero, the host is not reachable.


class Breadcrumb:
    """
    A class used to represent a Breadcrumb.

    This class holds the state and functionality for connecting, authenticating,
    and interacting with a host via a specific role. It maintains a dictionary of actions,
    roles and statuses.

    Attributes:
    host (str): The hostname or IP address of the target host.
    port (int): The port number to connect to at the target host.
    role (str): The role to use for interacting with the host.
    password (str): The password to use for authenticating the role.
    connection: Placeholder for a connection object. Initially set to None.
    serial: Placeholder for a serial number. Initially set to None.
    seq_number (int): The sequence number for actions sent to the host. Initially set to 0.
    actions (dict): A dictionary mapping action names to values, extracted from Message_pb2.BCMessage.Auth.Action.
    roles (dict): A dictionary mapping role names to values, extracted from Message_pb2.Common__pb2.Role.
    authenticated (bool): A flag indicating whether the Breadcrumb is currently authenticated. Initially set to False.
    statuses (dict): A dictionary mapping status codes to names, extracted from Message_pb2.BCMessage.Result.Status.
    """

    def __init__(self, *, host=None, port=None, role=None, password=None):
        """
        Constructs a new Breadcrumb instance.

        The parameters are all optional and each defaults to None if not provided.

        Parameters:
        host (str, optional): The hostname or IP address of the target host.
        port (int, optional): The port number to connect to at the target host.
        role (str, optional): The role to use for interacting with the host.
        password (str, optional): The password to use for authenticating the role.
        """
        self.host = host
        self.port = port
        self.role = role
        self.password = password
        self.connection = None
        self.serial = None
        self.seq_number = 0
        self.actions = {k: v for k, v in Message_pb2.BCMessage.Auth.Action.items()}
        self.roles = {k: v for k, v in Message_pb2.Common__pb2.Role.items()}
        self.authenticated = False
        self.statuses = {v: k for k, v in Message_pb2.BCMessage.Result.Status.items()}

    def reachable(self):
        """
        Checks if the host associated with this Breadcrumb instance is reachable.

        This method uses the is_host_reachable function to send a single ICMP echo
        request ("ping") to the host and determines reachability based on the success
        of that request.

        Returns:
        bool: True if the host is reachable (the ping command was successful), False otherwise.
        """
        return is_host_reachable(self.host)

    def get_message(self):
        """
        Retrieves and parses a message from the host associated with this Breadcrumb instance.

        This method receives a string from the host via the current connection,
        unpacks the data, and parses it into a BCMessage object (as defined in Message_pb2).
        The method also increments the sequence number attribute after parsing the message.

        Returns:
        Message_pb2.BCMessage: The parsed message from the host.

        Raises:
        An exception will be raised if there's a problem receiving or parsing the data.
        """
        message = Message_pb2.BCMessage()
        message.ParseFromString(unpack_data(self.connection.recv(65535)))
        self.seq_number += 1
        return message

    def build_message(self):
        """
        Constructs a new BCMessage object with a sequence number.

        This method creates a new BCMessage object (as defined in Message_pb2)
        and sets its sequence number to the current sequence number of this Breadcrumb instance.

        Returns:
        Message_pb2.BCMessage: The newly created BCMessage object.
        """
        message = Message_pb2.BCMessage()
        message.sequenceNumber = self.seq_number
        return message

    def send_message(self, message, gzip=False):
        """
        Sends a message to the host associated with this Breadcrumb instance.

        This method serializes the provided BCMessage object (as defined in Message_pb2),
        packs the serialized data (optionally compressing it with gzip), and sends it
        to the host via the current connection. The method also increments the sequence
        number attribute after sending the message.

        Parameters:
        message (Message_pb2.BCMessage): The message to be sent to the host.
        gzip (bool, optional): A flag indicating whether to compress the serialized data with gzip before sending it. Defaults to False.

        Raises:
        An exception will be raised if there's a problem packing or sending the data.
        """
        tx_packet = pack_data(message.SerializeToString(), gzip=gzip)
        self.connection.send(tx_packet)
        self.seq_number += 1

    def setup_connection_socket(self):
        """
        Sets up a secure socket connection to the host associated with this Breadcrumb instance.

        This method creates a new INET socket, sets a timeout of 2 seconds on the socket,
        wraps it in an SSL layer, and connects it to the host at the specified port.

        Raises:
        socket.error: If a socket error occurs.
        ssl.SSLError: If an SSL error occurs.
        """
        soc = socket(AF_INET)
        soc.settimeout(2)
        self.connection = wrap_socket(soc)
        self.connection.connect((self.host, self.port))

    def prepare_login_message(self, init_message):
        """
        Prepares a login message to authenticate with the host.

        This method builds a new BCMessage object with a sequence number, sets its action to "LOGIN",
        and its role to the Breadcrumb instance's role. It then computes a response hash from the
        password and the challenge received from the host (found in the provided init_message), and
        sets the response hash as the challengeOrResponse in the message. The compressionMask is set to 2.

        Parameters:
        init_message (Message_pb2.BCMessage): The initial message from the host, used to extract the challenge for response.

        Returns:
        Message_pb2.BCMessage: The prepared login message ready to be sent to the host.
        """
        # Create message to login and set the login role
        tx_message = self.build_message()
        tx_message.auth.action = self.actions["LOGIN"]
        tx_message.auth.role = self.roles[self.role]
        # create response (password + challenge received from radio) and hash for reply
        response_string = self.password + init_message.auth.challengeOrResponse.decode('latin1')
        response_hash = hashlib.sha384(response_string.encode('latin1')).digest()
        # set challengeOrResponse
        tx_message.auth.challengeOrResponse = response_hash
        tx_message.auth.compressionMask = 0 | 2
        return tx_message

    def authenticate(self):
        """
        Authenticates with the host associated with this Breadcrumb instance.

        This method first checks if the host is reachable. If it is, it sets up a socket connection,
        receives an initial message, and extracts the serial number. It then prepares and sends a login message,
        receives a result, and checks if the authentication was successful.

        In case of an error during this process, the method safely returns the current authentication status.

        Returns:
        bool: True if the authentication process was successful, False otherwise.
        """
        if self.reachable():
            try:

                self.setup_connection_socket()
                init_message = self.get_message()
                self.serial = str(init_message.auth.serial)
                self.send_message(self.prepare_login_message(init_message))
                status = self.statuses[self.get_message().authResult.status]

                if status == 'SUCCESS':
                    self.authenticated = True
                    return self.authenticated

                return self.authenticated
            except:
                return self.authenticated
        else:
            return self.authenticated

    def get_state(self):
        """
        Retrieves the state from the host associated with this Breadcrumb instance.

        This method first checks if the host is reachable and if the Breadcrumb instance is authenticated.
        If both conditions are met, it sends a request for the state, receives a response,
        and returns the state extracted from the response.

        If either the host is not reachable or the Breadcrumb instance is not authenticated, or if an error occurs
        during the process, it returns False.

        Returns:
        Message_pb2.BCMessage.State or bool: The state from the host if successful, False otherwise.
        """
        if self.reachable() and self.authenticated:
            try:
                request_state_message = self.build_message()
                request_state_message.state.Clear()
                self.send_message(request_state_message)
                response_message = self.get_message()
                return response_message.state
            except:
                return False
        else:
            return False

    def get_state_filter(self, filters):
        """
        Retrieves the state from the host associated with this Breadcrumb instance,
        filtered by the provided filters.

        This method first checks if the host is reachable and if the Breadcrumb instance is authenticated.
        If both conditions are met, it appends the filters to the stateFilterPath of the request message,
        sends a request for the state, receives a response, and returns the state extracted from the response.

        If either the host is not reachable or the Breadcrumb instance is not authenticated, or if an error occurs
        during the process, it either raises the exception or returns False.

        Parameters:
        filters (list): A list of filters to apply when requesting the state.

        Returns:
        Message_pb2.BCMessage.State or bool: The state from the host if successful, False otherwise.

        Raises:
        Exception: If any error occurs during the process, it will be raised.
        """
        if self.reachable() and self.authenticated:
            try:
                request_state_message = self.build_message()
                request_state_message.state.Clear()
                request_state_message.stateFilterPath.append(filters)
                self.send_message(request_state_message)
                response_message = self.get_message()
                return response_message.state
            except Exception as e:
                raise e
        else:
            return False