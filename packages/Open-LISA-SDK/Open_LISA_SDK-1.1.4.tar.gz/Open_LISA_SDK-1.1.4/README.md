# Open LISA SDK

This repository is part of [Open LISA project](https://github.com/open-lisa):
* [Open LISA Server](https://github.com/open-lisa/Open-LISA-Server)
* [Open LISA SDK](https://github.com/open-lisa/Open-LISA-SDK)
* [Open LISA UI](https://github.com/open-lisa/Open-LISA-UI)


This SDK provides an interface to interact with the [Open LISA Server](https://github.com/open-lisa/Open-LISA-Server). The server must be integrated with the instruments of interest and running in a known Serial port (RS233 connections) in order to be able to connect via this SDK from the client side. Alternatively, you can use TCP protocol for communication being aware that this system does not provide authentication or encryption under this protocol.

## Installation

```
pip install open-lisa-sdk
```

## Getting started

After installation and having configured the server with the instruments, you are ready create your experience scripts with Open LISA SDK in a few lines of code. For example:

1. Connect with the server

```python
import Open_LISA_SDK

sdk = Open_LISA_SDK.SDK()
sdk.connect_through_RS232(port="COM3")
```

2. Get the instruments

```python
instruments = sdk.get_instruments()
for instrument in instruments:
    print("instrument {} {}".format(instrument["brand"], instrument["model"]))
```

3. Get instrument commands and send invocations to your instruments

```python
instruments = sdk.get_instruments()
first_instrument = instruments[0]
command_execution_result = sdk.send_command(instrument_id=first_instrument["id"], command_invocation="set_channel_volts 1 5.0")
print(command_execution_result)
```

4. After finishing, remember to disconnect

```python
sdk.disconnect()
```

## Examples

You can check more online examples [here](./examples). Go to `examples` folder and just run

```bash
python <example_script_name>.py
```

## API Doc

You can check the full Open LISA SDK API Doc [here](./docs/api-doc/README.md), as well as the full source code in its [repository](https://github.com/open-lisa/Open-LISA-SDK)
