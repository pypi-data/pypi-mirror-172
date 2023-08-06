# NOTE: this tests expect the Open LISA Server being run in TCP mode
# at port 8080 and with ENV=test
# Example: python main.py  --env test --mode TCP --tcp_port 8080 --log-level INFO
import json

import pytest

from ..domain.exceptions.could_not_connect_to_server import CouldNotConnectToServerException

from ..domain.exceptions.sdk_exception import OpenLISAException
from .. import SDK

LOCALHOST = "127.0.0.1"
SERVER_PORT = 8080
LOG_LEVEL = "ERROR"
TEST_TEKTRONIX_OSC_PHYSICAL_ADDRESS = "USB0::0x0699::0x0363::C107676::INSTR"
TEST_TEKTRONIX_OSC_INSTRUMENT_ID = 1
MOCK_CAMERA_ID = 2
UNEXISTING_INSTRUMENT_ID = 999
SOME_VALID_TEKTRONIX_OSC_COMMAND = "clear_status"
SOME_VALID_TEKTRONIX_OSC_COMMAND_INVOCATION = "clear_status"
MOCK_IMAGE_PATH = "Open_LISA_SDK/tests/mock_img.jpg"

VALID_INSTRUMENT_CREATION_DICT = {
    "brand": "some brand",
    "model": "some model",
    "physical_address": None,
    "type": "CLIB",
    "description": "some description"
}
VALID_UPDATED_BRAND = "some new brand"
VALID_INSTRUMENT_UPDATE_DICT = {
    "brand": VALID_UPDATED_BRAND
}


def test_get_instruments_as_python_list_of_dicts():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments(response_format="PYTHON")
    assert isinstance(instruments, list)
    for i in instruments:
        assert isinstance(i, dict)
    sdk.disconnect()


def test_get_instruments_as_json_string():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments_json_string = sdk.get_instruments(response_format="JSON")
    assert isinstance(instruments_json_string, str)

    try:
        json.loads(instruments_json_string)
    except:
        pytest.fail("invalid json string received: {}".format(
            instruments_json_string))

    sdk.disconnect()


def test_lock_is_released_after_exceptions():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    with pytest.raises(OpenLISAException):
        sdk.get_instrument(instrument_id=UNEXISTING_INSTRUMENT_ID,
                           response_format="PYTHON")
    with pytest.raises(OpenLISAException):
        sdk.get_instrument(instrument_id=UNEXISTING_INSTRUMENT_ID,
                           response_format="PYTHON")


def test_get_specific_instrument_as_python_dict():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instrument = sdk.get_instrument(
        instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID, response_format="PYTHON")
    assert isinstance(instrument, dict)
    assert instrument["physical_address"] == TEST_TEKTRONIX_OSC_PHYSICAL_ADDRESS

    sdk.disconnect()


def test_get_specific_instrument_as_json_str():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instrument_json = sdk.get_instrument(
        instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID, response_format="JSON")
    assert isinstance(instrument_json, str)
    assert TEST_TEKTRONIX_OSC_PHYSICAL_ADDRESS in instrument_json

    sdk.disconnect()


def test_get_specific_instrument_that_does_not_exist_raises_exception():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    with pytest.raises(OpenLISAException):
        sdk.get_instrument(instrument_id=UNEXISTING_INSTRUMENT_ID,
                           response_format="PYTHON")
    sdk.disconnect()


def test_get_instrument_commands_as_python_list_of_dicts():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    commands = sdk.get_instrument_commands(
        instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID, response_format="PYTHON")
    assert isinstance(commands, dict)
    assert SOME_VALID_TEKTRONIX_OSC_COMMAND in commands.keys()
    sdk.disconnect()


def test_get_instrument_commands_as_json_string():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    commands_json_string = sdk.get_instrument_commands(
        instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID, response_format="JSON")
    assert isinstance(commands_json_string, str)
    assert SOME_VALID_TEKTRONIX_OSC_COMMAND in commands_json_string
    sdk.disconnect()


def test_is_valid_command_invocation_with_a_valid_invocation_returns_true():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    is_valid = sdk.is_valid_command_invocation(
        instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID,
        command_invocation=SOME_VALID_TEKTRONIX_OSC_COMMAND_INVOCATION)
    assert is_valid == True
    sdk.disconnect()


def test_is_valid_command_invocation_with_invalid_invocations_returns_false():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    invalid_invocations = [
        "unexisting command",
        "set_trigger_level 10 20",
        "set_trigger_level ASCII",
    ]
    for ii in invalid_invocations:
        is_valid = sdk.is_valid_command_invocation(
            instrument_id=TEST_TEKTRONIX_OSC_INSTRUMENT_ID,
            command_invocation=ii)
        print(ii)
        assert is_valid == False
    sdk.disconnect()


def test_send_command_to_get_image_from_mock_camera():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    result = sdk.send_command(instrument_id=MOCK_CAMERA_ID,
                              command_invocation="get_image")
    with open(MOCK_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
        assert image_bytes == result["value"]


def test_send_command_and_save_result_in_server():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    result = sdk.send_command(instrument_id=MOCK_CAMERA_ID,
                              command_invocation="get_image", command_result_output_file="sandbox/output.jpg")
    assert result == None
    sandbox_dir = sdk.get_directory_structure(
        "sandbox", response_format="PYTHON")
    # TODO: assert here that output.jpg exists in server
    sdk.delete_file(file_path="sandbox/output.jpg")
    sandbox_dir = sdk.get_directory_structure(
        "sandbox", response_format="PYTHON")
    # TODO: assert here that output.jpg does not exist in server


def test_instrument_CRUDs():
    sdk = SDK(log_level=LOG_LEVEL)
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    new_instrument = sdk.create_instrument(
        new_instrument=VALID_INSTRUMENT_CREATION_DICT, response_format="PYTHON")
    assert new_instrument["brand"] == VALID_INSTRUMENT_CREATION_DICT["brand"]

    updated_instrument = sdk.update_instrument(
        instrument_id=new_instrument["id"], updated_instrument=VALID_INSTRUMENT_UPDATE_DICT, response_format="PYTHON")
    assert new_instrument["id"] == updated_instrument["id"]
    assert updated_instrument["brand"] == VALID_INSTRUMENT_UPDATE_DICT["brand"]

    deleted_instrument = sdk.delete_instrument(
        instrument_id=new_instrument["id"], response_format="PYTHON")
    assert new_instrument["id"] == deleted_instrument["id"]

    with pytest.raises(OpenLISAException):
        sdk.get_instrument(instrument_id=deleted_instrument["id"])

    sdk.disconnect()
