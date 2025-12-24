import zmq
ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.connect("tcp://127.0.0.1:2222")
s.send(b"test")
print(s.recv())
