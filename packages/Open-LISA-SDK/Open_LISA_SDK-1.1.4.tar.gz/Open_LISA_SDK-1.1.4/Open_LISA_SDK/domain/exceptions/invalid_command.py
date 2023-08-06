from .sdk_exception import OpenLISAException

DEFAULT_MESSAGE = "invalid command"

class InvalidCommandException(OpenLISAException):
  """
    Raised when the SDK is initiated and connection with server could not be established
  """
  def __init__(self, message=DEFAULT_MESSAGE):
    self.message = message
    super().__init__(self.message)