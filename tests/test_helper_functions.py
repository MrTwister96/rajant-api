import unittest
import rajant_api


class TestIsHostReachable(unittest.TestCase):

    def test_reachable_host(self):
        """
        Test that the function returns True when the host is reachable.
        """
        # Use a known reachable host, such as "8.8.8.8" (Google's DNS server)
        self.assertTrue(rajant_api.is_host_reachable("8.8.8.8"))

    def test_unreachable_host(self):
        """
        Test that the function returns False when the host is not reachable.
        """
        # Use a known unreachable host
        self.assertFalse(rajant_api.is_host_reachable("0.0.0.0"))

    def test_invalid_host(self):
        """
        Test that the function raises ValueError when the host is invalid.
        """
        with self.assertRaises(ValueError):
            rajant_api.is_host_reachable("invalid_host")


class TestGPS(unittest.TestCase):
    def test_gps_enabled(self):
        class state:  # Define a mock state object with the necessary attributes
            class gps:
                class gpsSwitch:
                    enabled = True

                class gpsPos:
                    gpsLat = "2743.8950S"
                    gpsLong = "02258.1429E"

        result = rajant_api.helper_functions.get_gps(state)

        expected_result = {
            'enabled': True,
            'latitude': -27.731583333333333,
            'longitude': 22.969048333333333
        }
        self.assertEqual(result, expected_result)

    def test_gps_disabled(self):
        class state:  # Define a mock state object with the necessary attributes
            class gps:
                class gpsSwitch:
                    enabled = False

                class gpsPos:
                    gpsLat = "000000000"
                    gpsLong = "0000000000"

        result = rajant_api.helper_functions.get_gps(state)
        expected_result = {
            'enabled': False,
            'latitude': 0,
            'longitude': 0
        }
        self.assertEqual(result, expected_result)


class TestIPAddress(unittest.TestCase):
    def test_valid_ipv4(self):
        self.assertTrue(rajant_api.helper_functions.is_valid_ipv4("127.0.0.1"))  # Test a valid IP address

    def test_invalid_ipv4(self):
        self.assertFalse(
            rajant_api.helper_functions.is_valid_ipv4("256.1.1.1"))  # Test an invalid IP address (256 is out of range)

    def test_non_string_input(self):
        self.assertFalse(rajant_api.helper_functions.is_valid_ipv4(12345))  # Test a non-string input

    def test_empty_string(self):
        self.assertFalse(rajant_api.helper_functions.is_valid_ipv4(""))  # Test an empty string


class TestPackUnpackData(unittest.TestCase):
    def test_pack_unpack_data(self):
        # Test with gzip compression
        data = b"This is some test data"
        packet = rajant_api.helper_functions.pack_data(data, gzip=True)
        self.assertEqual(rajant_api.helper_functions.unpack_data(packet), data)

        # Test without gzip compression
        packet = rajant_api.helper_functions.pack_data(data, gzip=False)
        self.assertEqual(rajant_api.helper_functions.unpack_data(packet), data)

    def test_pack_data_with_invalid_input(self):
        # Test with non-bytes input
        with self.assertRaises(ValueError):
            rajant_api.helper_functions.pack_data("This is a string, not bytes", gzip=False)

    def test_unpack_data_with_invalid_input(self):
        # Test with a packet that's too short
        with self.assertRaises(ValueError):
            rajant_api.helper_functions.unpack_data(b"\x00")

        # Test with a packet that has an unknown compression flag
        with self.assertRaises(ValueError):
            packet = b"\x00\x00\x00\x00\x01\x00\x00\x00" + b"This is some test data"
            rajant_api.helper_functions.unpack_data(packet)


if __name__ == '__main__':
    unittest.main()
