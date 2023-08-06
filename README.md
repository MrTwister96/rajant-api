# rajant-api 

A Python library that provides an interface for developers to communicate with Rajant Breadcrumb radios. The rajant-api library allows users to retrieve the state and configuration of these radios and to make changes to the configuration.

## Installation 

The library can be installed via pip:
```shell
pip install rajant-api
```

## Usage

Here's a basic example of using the library to connect to a radio, authenticate and retrieve its state:

```python
from rajant_api import Breadcrumb

bc = Breadcrumb(host="192.168.0.20",
				port=2300,
				role="VIEW",
				password="view-password")
				
if bc.authenticate():
    print(bc.get_state())
```

## Breadcrumb class

The main class exposed by this library is Breadcrumb. It holds the state and functionality for connecting, authenticating, and interacting with a host via a specific role. Here are the available methods:

### `reachable()`

Checks if the host associated with this Breadcrumb instance is reachable.

### `get_message()`

Retrieves and parses a message from the host associated with this Breadcrumb instance.

### `build_message()`

Constructs a new BCMessage object with a sequence number.

### `send_message()`

Sends a message to the host associated with this Breadcrumb instance.

### `setup_connection_socket()`

Sets up a secure socket connection to the host associated with this Breadcrumb instance.

### `prepare_login_message()`

Prepares a login message to authenticate with the host.

### `authenticate()`

Authenticates with the host associated with this Breadcrumb instance.

### `get_state()`

Retrieves the state from the host associated with this Breadcrumb instance.

### `get_state_filter()`

Retrieves the state from the host associated with this Breadcrumb instance, filtered by the provided filters.

## Contributing

Contributions are welcome! Please open an issue if you encounter any problems or have suggestions for improvements.

## License

[Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode)