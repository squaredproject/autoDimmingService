import json, socket

class Server(object):
  """
  A JSON socket server used to communicate with a JSON socket client. All the
  data is serialized in JSON. How to use it:

  server = Server(host, port)
  while True:
    server.accept()
    data = server.recv()
    # shortcut: data = server.accept().recv()
    server.send({'status': 'ok'})
  """

  backlog = 5
  client = None

  def __init__(self, host, port):
    self.socket = socket.socket()
    self.socket.bind((host, port))
    self.socket.listen(self.backlog)

  def __del__(self):
    self.close()

  def accept(self):
    # if a client is already connected, disconnect it
    if self.client:
      self.client.close()
    self.client, self.client_addr = self.socket.accept()
    return self

  def send(self, data):
    if not self.client:
      raise Exception('Cannot send data, no client is connected')
    _send(self.client, data)
    return self

  def recv(self):
    if not self.client:
      raise Exception('Cannot receive data, no client is connected')
    return _recv(self.client)

  def close(self):
    if self.client:
      self.client.close()
      self.client = None
    if self.socket:
      self.socket.close()
      self.socket = None


class Client(object):
  """
  A JSON socket client used to communicate with a JSON socket server. All the
  data is serialized in JSON. How to use it:

  data = {
    'name': 'Patrick Jane',
    'age': 45,
    'children': ['Susie', 'Mike', 'Philip']
  }
  client = Client()
  client.connect(host, port)
  client.send(data)
  response = client.recv()
  # or in one line:
  response = Client().connect(host, port).send(data).recv()
  """

  socket = None

  def __del__(self):
    self.close()

  def connect(self, host, port):
    self.socket = socket.socket()
    self.socket.connect((host, port))
    self.socket.settimeout(3)
    return self

  def send(self, data):
    if not self.socket:
      raise Exception('You have to connect first before sending data')
    _send(self.socket, data)
    return self

  def recv(self):
    if not self.socket:
      raise Exception('You have to connect first before receiving data')
    return _recv(self.socket)

  def recv_and_close(self):
    data = self.recv()
    self.close()
    return data

  def close(self):
    if self.socket:
      self.socket.close()
      self.socket = None


## helper functions ##

def _send(socket, data):
  try:
    serialized = json.dumps(data)
  except (TypeError, ValueError) as e:
    raise Exception('You can only send JSON-serializable data')
#  print(f'serialized type {type(serialized)}')
  b = bytes( serialized + '\n', 'ascii')
  socket.sendall(b)

def _recv(socket):
  # read the length of the data, letter by letter until we reach EOL
  data_in = ''
  char = socket.recv(1).decode('ascii')
  while char != '\n':
    data_in += char
    char = socket.recv(1).decode('ascii')
  try:
    deserialized = json.loads(data_in)
  except (TypeError, ValueError) as e:
    raise Exception('Data received was not in JSON format')
  return deserialized
