import asyncio
from asyncio import Transport
from datetime import datetime


class AbstractServerProtocol(asyncio.Protocol):
    def connection_made(self, transport: Transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport  # noqa

    def connection_lost(self, exc: Exception | None):
        if exc is None:
            self.transport.close()

    def data_received(self, data: bytes):
        message = data.decode()
        print("Data received: {!r}".format(message))
        self._send(data)

        print("Close the client socket")
        self.transport.close()

    def _send(self, data: bytes):
        raise NotImplementedError


class EchoServerProtocol(AbstractServerProtocol):
    # Do not use Safari, use Mozilla
    def _send(self, data: bytes):
        self.transport.write(data)
        print("Send: {!r}".format(data))


class HelloWorldServerProtocol(AbstractServerProtocol):
    def _send(self, _):
        date_header = format(datetime.now(), "%a, %d %b %Y %H:%M:%S %Z").encode("utf-8")
        self.transport.write(b"HTTP/1.1 200 OK\r\ndate: " + date_header + b"\r\nserver: "
                             b"uvicorn\r\ncontent-type: text/plain\r\nTransfer-Encoding: chunked\r\n\r\n")
        self.transport.write(b"d\r\nHello, world!\r\n")
        self.transport.write(b"0\r\n\r\n")

        print("Send: Hello, world!")


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        protocol_factory=lambda: EchoServerProtocol(),
        # lambda: HelloWorldServerProtocol(),
        host="127.0.0.1", port=8000)

    async with server:
        await server.serve_forever()


asyncio.run(main())
