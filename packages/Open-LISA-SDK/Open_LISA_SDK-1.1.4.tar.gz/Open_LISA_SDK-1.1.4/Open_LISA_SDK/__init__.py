import json
import socket
from threading import Lock
import traceback
import serial
import serial.tools.list_ports

from .domain.decorators.with_lock import with_lock
from .domain.exceptions.invalid_command import InvalidCommandException
from .domain.protocol.client_protocol import ClientProtocol
from .domain.exceptions.could_not_connect_to_server import CouldNotConnectToServerException

from .common.protocol.message_protocol_rs232 import MessageProtocolRS232
from .common.protocol.message_protocol_tcp import MessageProtocolTCP

from .logging import log

DEFAULT_RS232_BAUDRATE = 921600

SDK_RESPONSE_FORMAT_JSON = "JSON"
SDK_RESPONSE_FORMAT_PYTHON = "PYTHON"
SDK_VALID_RESPONSE_FORMATS = [
    SDK_RESPONSE_FORMAT_JSON, SDK_RESPONSE_FORMAT_PYTHON]

CONVERT_TO_STRING = "str"
CONVERT_TO_DOUBLE = "double"
CONVERT_TO_BYTEARRAY = "bytearray"
CONVERT_TO_BYTES = "bytes"
CONVERT_TO_INT = "int"

AVAILABLE_CONVERT_TYPES = [
    CONVERT_TO_STRING,
    CONVERT_TO_DOUBLE,
    CONVERT_TO_BYTEARRAY,
    CONVERT_TO_BYTES,
    CONVERT_TO_INT,
]

LOCK = Lock()


class SDK:
    """
    SDK for interact with Open LISA Server
    """

    def __init__(self, log_level="WARNING", default_response_format=SDK_RESPONSE_FORMAT_PYTHON):
        """
        Initializes the SDK with the specified log level and default response format of the methods

        Args:
            log_level (str, optional): specifies the SDK log level. Defaults to "WARNING".
            default_response_format (str, optional): specifies the response format of the SDK methods supported
            types are "PYTHON" for Python native types or "JSON" for JSON strings. Defaults to "PYTHON".
        """
        log.set_level(log_level)
        log.info("Initializating SDK")

        self._default_response_format = default_response_format

    @with_lock(LOCK)
    def connect_through_TCP(self, host: str, port: int) -> None:
        """Tries to connect with Open LISA Server through TCP protocol

        Args:
            host (string): Open LISA Server IP address
            port (int): Open LISA Server port number

        Raises:
            CouldNotConnectToServerException: raised when connection could not be stablished
        """
        try:
            CONNECTION_TIMEOUT = 5
            server_address = (host, int(port))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(CONNECTION_TIMEOUT)
            sock.connect(server_address)
            sock.settimeout(None)
            self._client_protocol = ClientProtocol(MessageProtocolTCP(sock))
        except Exception as e:
            log.error(e)
            raise CouldNotConnectToServerException(
                "could not connect with server at {} through TCP".format(server_address))

    @with_lock(LOCK)
    def connect_through_RS232(self, baudrate=DEFAULT_RS232_BAUDRATE, port=None) -> None:
        """Tries to connect with Open LISA Server through RS232 protocol

        Args:
            baudrate (int, optional): Specifies the baudrate, must be the same as in Open LISA Server. Defaults to 921600.
            port (str, optional): Serial port of the client side. Defaults to None and will try with all the ports listed by serial.tools.list_ports.comports(),
            this is not recommended since handshake information could be sent to unexpected serial ports.

        Raises:
            CouldNotConnectToServerException: raised when connection could not be stablished
        """
        # Discover server RS232
        TIMEOUT_TO_WAIT_HANDSHAKE_RESPONSE = 3

        connection = None
        detected_ports_info_instances = serial.tools.list_ports.comports()
        detected_port_devices = [
            pinfo.device for pinfo in detected_ports_info_instances]
        ports_to_try = detected_port_devices if not port else [port]
        for port in ports_to_try:
            try:
                log.debug(
                    '[connect_through_RS232] trying to connect to {}'.format(port))
                connection = serial.Serial(
                    port=port, baudrate=baudrate, timeout=TIMEOUT_TO_WAIT_HANDSHAKE_RESPONSE)

                log.debug(
                    '[connect_through_RS232] connection created {}'.format(connection))
                if not connection.is_open:
                    connection.open()

                try:
                    self._client_protocol = ClientProtocol(
                        MessageProtocolRS232(rs232_connection=connection))
                    self._client_protocol.health_check()
                except Exception as e:
                    log.info(
                        '[connect_through_RS232] fail doing healthcheck at port {}, exception {}'.format(port, e))
                    self._client_protocol = None
                    continue
            except serial.SerialException as ex:
                log.info('serial exception {}'.format(ex))
                log.debug('exception stacktrace {}'.format(
                    traceback.format_exc()))
                log.debug("could not connect to {}".format(port))
                connection = None

        if not self._client_protocol:
            raise CouldNotConnectToServerException(
                "could not detect Open LISA server listening through RS232")

    @with_lock(LOCK)
    def disconnect(self):
        """Gracefully disconnect with Open LISA Server
        """
        self._client_protocol.disconnect()

    @with_lock(LOCK)
    def __reset_databases(self):
        return self._client_protocol.reset_databases()

    @with_lock(LOCK)
    def create_instrument(self, new_instrument, response_format=None):
        """Tries to create the new instrument with the fields specified

        Args:
            new_instrument (dict): new instrument payload
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|string: server creation response

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        created_instrument_as_json_string = self._client_protocol.create_instrument_as_json_string(
            new_instrument)
        return self.__format_response(created_instrument_as_json_string, response_format)

    @with_lock(LOCK)
    def update_instrument(self, instrument_id, updated_instrument, response_format=None):
        """Tries to update the instrument with the fields specified

        Args:
            instrument_id (int): instrument ID
            updated_instrument (dict): new instrument fields
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|string: server update response

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        updated_instrument_as_json_string = self._client_protocol.update_instrument_as_json_string(
            instrument_id, updated_instrument)
        return self.__format_response(updated_instrument_as_json_string, response_format)

    @with_lock(LOCK)
    def delete_instrument(self, instrument_id, response_format=None):
        """Tries to delete the instrument specified

        Args:
            instrument_id (int): instrument ID
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|string: server delete response

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        deleted_instrument = self._client_protocol.delete_instrument_as_json_string(
            instrument_id)
        return self.__format_response(deleted_instrument, response_format)

    @with_lock(LOCK)
    def get_instruments(self, response_format=None):
        """Get all the instruments registered in Open LISA Server

        Args:
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|string: list of registered instruments

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        instruments_as_json_string = self._client_protocol.get_instruments_as_json_string()
        return self.__format_response(instruments_as_json_string, response_format)

    @with_lock(LOCK)
    def get_instrument(self, instrument_id, response_format=None):
        """Get the instrument registered in Open LISA Server that matches with the ID

        Args:
            instrument_id (int): instrument ID
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|string: the instrument match
        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        instrument_as_json_string = self._client_protocol.get_instrument_as_json_string(
            instrument_id)
        return self.__format_response(instrument_as_json_string, response_format)

    @with_lock(LOCK)
    def get_detected_physical_addresses(self, response_format=None):
        """Get a list of the detected physical addresses in the Open LISA Server

        Args:
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            list|string: the physical addresses detected

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        detected_physical_addresses_as_json_string = self._client_protocol.get_detected_physical_addresses()
        return self.__format_response(detected_physical_addresses_as_json_string, response_format)

    @with_lock(LOCK)
    def get_instrument_commands(self, instrument_id, response_format=None):
        """Get a list of the specified instrument commands

        Args:
            instrument_id (int): instrument ID
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            list|stirng: The list of the registered commands for that instrument

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        commands_as_json_string = self._client_protocol.get_instrument_commands_as_json_string(
            id=instrument_id)
        return self.__format_response(commands_as_json_string, response_format)

    @with_lock(LOCK)
    def is_valid_command_invocation(self, instrument_id, command_invocation):
        """Determines if the command invocation syntax is valid but it is not sent to the instrument

        Args:
            instrument_id (int): instrument ID
            command_invocation (str): command invocation syntax

        Returns:
            bool: True or False depending the validity of the command invocation syntax
        """
        try:
            self._client_protocol.validate_command(
                instrument_id, command_invocation)
            print("{} is OK".format(command_invocation))
            return True
        except InvalidCommandException as e:
            print(e)
            return False

    @with_lock(LOCK)
    def send_command(self, instrument_id, command_invocation, command_result_output_file=None, response_format=None,
                     convert_result_to=None):
        """Sends the command_invocation to the specified instrument by instrument_id

        Args:
            instrument_id (int): instrument ID
            command_invocation (str): command invocation syntax with parameters
            command_result_output_file (str, optional): if provided the output of the command will be saved in server at the specified path and
            not returned to the client (convinient for low throughputs between client and server). Defaults to None.
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case
            convert_result_to (str, optional): converts the result to the specified type, supported types are "str", "double", "bytearray", "bytes" and "int". Defaults to None.

        Raises:
            InvalidCommandException: when the command could not be executed

        Returns:
            str|int|float|bytearray|bytes: the result of the command execution
        """
        if response_format == SDK_RESPONSE_FORMAT_JSON or (
                response_format == None and self._default_response_format == SDK_RESPONSE_FORMAT_JSON):
            # If response format is json convert_result_to is ignored
            return self._client_protocol.send_command_and_result_as_json_string(instrument_id, command_invocation,
                                                                                command_result_output_file)

        command_execution_result = self._client_protocol.send_command(
            instrument_id, command_invocation, command_result_output_file)

        if not convert_result_to or command_result_output_file:
            return command_execution_result

        original_value = command_execution_result["value"]
        try:
            if convert_result_to == CONVERT_TO_STRING:
                command_execution_result["value"] = str(original_value)
            elif convert_result_to == CONVERT_TO_INT:
                command_execution_result["value"] = \
                    int(float((original_value)))
            elif convert_result_to == CONVERT_TO_DOUBLE:
                command_execution_result["value"] = float(original_value)
            elif convert_result_to == CONVERT_TO_BYTEARRAY:
                command_execution_result["value"] = bytearray(original_value)
            elif convert_result_to == CONVERT_TO_BYTES:
                command_execution_result["value"] = bytes(original_value)

        except ValueError as e:
            error = "could not convert '{}' to type '{}'.".format(
                original_value, convert_result_to)
            log.error(error)
            raise InvalidCommandException(error)

        return command_execution_result

    @with_lock(LOCK)
    def send_file(self, file_path, file_target_name):
        """Sends the file specified by client file_path and saves it in the server at file_target_name

        Args:
            file_path (str): client side file path
            file_target_name (_type_): server remote file path

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        with open(file_path, "rb") as file:
            data = file.read()
            return self._client_protocol.send_file(data, file_target_name)

    @with_lock(LOCK)
    def delete_file(self, file_path):
        """Deletes the remote file specified by file_path

        Args:
            file_path (str): file path in server

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.delete_file(file_path)

    @with_lock(LOCK)
    def get_file(self, remote_file_name, file_target_name):
        """Tries to retrieve the file in server specified by remote_file_name and tries to save in file_target_name in client side

        Args:
            remote_file_name (str): file path in server
            file_target_name (str): file path in client

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        file_bytes = self._client_protocol.get_file(remote_file_name)
        with open(file_target_name, "wb") as file:
            file.write(file_bytes)

    @with_lock(LOCK)
    def get_directory_structure(self, remote_path, response_format=None):
        """Retrieves the directory structure in server specified in remote_path

        Args:
            remote_path (str): directory path in server side
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Returns:
            dict|str: directory structure

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        directory_structure = self._client_protocol.get_directory_structure_as_json_string(
            remote_path)
        return self.__format_response(directory_structure, response_format)

    @with_lock(LOCK)
    def create_directory(self, remote_path, new_directory):
        """Creates a folder with the name specified by new_directory in remote_path folder

        Args:
            remote_path (str): folder in server side
            new_directory (str): new folder name

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.create_directory(remote_path, new_directory)

    @with_lock(LOCK)
    def delete_directory(self, remote_path):
        """Deletes the folder specified by remote_path and all its content

        Args:
            remote_path (str): path in server side

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.delete_directory(remote_path)

    @with_lock(LOCK)
    def execute_bash_command(self, command, capture_stdout=False, capture_stderr=False):
        """Executes the bash command specified by command in the server

        Args:
            command (str): bash command to be executed in server side, the command is executed at sandbox folder
            capture_stdout (bool, optional): if true the stdout of the command is retrieved. Defaults to False.
            capture_stderr (bool, optional): if true the stderr of the command is retrieved. Defaults to False.

        Returns:
            any: command execution result
        """
        return self._client_protocol.execute_bash_command(command, capture_stdout, capture_stderr)

    @with_lock(LOCK)
    def create_instrument_command(self, new_command, response_format=None):
        """Creates the command specified by new_command payload

        Args:
            new_command (dict): new command payload
            response_format (str, optional): specifies response format. Defaults to None and default_response_format will be used in that case

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        command_type = new_command["type"]
        assert command_type in ["SCPI", "CLIB"]

        created_command_as_json_string = \
            self._client_protocol.create_instrument_command_as_json_string(
                new_command=new_command)

        return self.__format_response(created_command_as_json_string, response_format)

    @with_lock(LOCK)
    def delete_instrument_command(self, command_id):
        """Deletes the command specified by command_id

        Args:
            command_id (int): command ID

        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.delete_instrument_command(command_id)

    @with_lock(LOCK)
    def set_instrument_visa_attribute(self, instrument_id, attribute, state):
        """Sets the state of the attribute of the instrument with ID instrument_id

        Args:
            instrument_id (int): instrument ID
            attribute (Any): the VISA attribute to set
            state (str): the state to set

        Returns:
            str: status of the set operation
        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.set_instrument_visa_attribute(instrument_id, attribute, state)

    @with_lock(LOCK)
    def get_instrument_visa_attribute(self, instrument_id, attribute):
        """Gets the state of the attribute of the instrument with ID instrument_id

        Args:
            instrument_id (int): instrument ID
            attribute (Any): the VISA attribute to get

        Returns:
            Any: state of the attribute
        Raises:
            OpenLISAException: raised when there was an error in the Server
        """
        return self._client_protocol.get_instrument_visa_attribute(instrument_id, attribute)

    def __format_response(self, json_string, response_format):
        response_format = response_format if response_format else self._default_response_format
        assert response_format in SDK_VALID_RESPONSE_FORMATS
        if response_format == SDK_RESPONSE_FORMAT_JSON:
            return json_string
        elif response_format == SDK_RESPONSE_FORMAT_PYTHON:
            return json.loads(json_string)
