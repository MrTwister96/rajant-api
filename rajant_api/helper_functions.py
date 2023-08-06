import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

#     IP Address Utilities     #

import ipaddress


def is_valid_ipv4(address):
    """
    Checks if a string is a valid IPv4 address.

    Parameters:
    address (str): The string to check.

    Returns:
    bool: True if the string is a valid IPv4 address, False otherwise.
    """
    try:
        ipaddress.IPv4Address(str(address))
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


################################


#     TCP Packet Formation     #

from struct import pack, unpack, error as struct_error
from zlib import decompress, compress, error as zlib_error


def pack_data(data, gzip=False):
    """
    Pack the given data into a binary packet with an optional gzip compression.
    """
    if not isinstance(data, bytes):
        raise ValueError("data must be of type 'bytes'")
    if gzip:
        try:
            data = compress(data)
        except zlib_error:
            raise ValueError("Failed to compress data")
    header = pack('>ibbbb', len(data), 2 if gzip else 0, 0, 0, 0)
    packet = header + data
    return packet


def unpack_data(packet):
    """
    Unpack the data from a binary packet, possibly decompressing if gzip-compressed.
    """
    if not isinstance(packet, bytes):
        raise ValueError("Input must be bytes.")
    if len(packet) < 8:
        raise ValueError("Input must be at least 8 bytes long.")



    try:
        header = unpack('>ibbbb', packet[:8])
    except struct_error:
        raise ValueError("Failed to unpack header")

    data = packet[8:]

    if header[1] == 2:
        try:
            data = decompress(data)
        except zlib_error:
            raise ValueError("Failed to decompress data")
    elif header[1] != 0:
        raise ValueError(f"Unknown compression flag: {header[1]}")

    return data


################################


#       bcapi helpers          #

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
    try:
        if hasattr(state, "gps") and hasattr(state.gps, "gpsSwitch") and state.gps.gpsSwitch.enabled:
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
    except AttributeError:
        logger.error("The state object does not have the expected attributes.")
        return None
    except ValueError:
        logger.error("The GPS data could not be converted to floats.")
        return None
    except TypeError:
        logger.error("The GPS data are not the expected types.")
        return None


################################


#      Connectivity Helpers      #

import platform
import subprocess


def is_host_reachable(host):
    """
    Checks if a host is reachable by sending a single ICMP echo request ("ping") to the host.

    Parameters:
    host (str): The hostname or IP address of the target host.

    Returns:
    bool: True if the host is reachable (the ping command was successful), False otherwise.

    Raises:
    ValueError: If host is not a valid IPv4 address.
    Exception: If an unexpected error occurs.
    """

    if not is_valid_ipv4(host):
        raise ValueError('Host must be a valid IPv4 address')

    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", host]
    else:
        cmd = ["ping", "-c", "1", host]

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        logger.exception("An unexpected error occurred")
        raise

#######################################
