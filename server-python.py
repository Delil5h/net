import logging
import asyncio
import parse

APP_LOGGER = logging.getLogger(name="HTTP server")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s]%(name)s : %(asctime)s > %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)

class HTTPServer:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def handle_request(self):
        request = await self.reader.read(2048)
        request_value = request.decode()
        APP_LOGGER.debug(f"Received request: {request_value.strip()}")

        lines = request_value.splitlines()
        if not lines:
            return

        try:
            method, path, _ = lines[0].split()
        except ValueError:
            await self.send_error(400, "Bad Request")
            return

        parsed_url = urlparse(path)  # Use the imported function directly
        parsed_path = parsed_url.path

        if parsed_path == "/":
            await self.send_template("index.html")
        elif parsed_path == "/register":
            await self.send_template("register.html")
        elif parsed_path == "/submit" and method == "POST":
            await self.handle_registration(request_value)
        else:
            await self.send_error(404, "Not Found")

    async def send_template(self, filename):
        try:
            with open(f"templates/{filename}", "r") as f:
                content = f.read()
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(content.encode())}\r\n"
                "\r\n"
                f"{content}"
            )
            self.writer.write(response.encode())
            await self.writer.drain()
        except FileNotFoundError:
            await self.send_error(404, "Not Found")
        except Exception as e:
            APP_LOGGER.error(f"Error sending template {filename}: {e}")
            await self.send_error(500, "Internal Server Error")

    async def handle_registration(self, request_value):
        try:
            _, body = request_value.split("\r\n\r\n", 1)
            parsed_body = parse_qs(body)  # Use the imported function directly
            username = parsed_body.get("username", [""])[0]
            email = parsed_body.get("email", [""])[0]

            if username and email:
                with open("db.txt", "a") as f:
                    f.write(f"{username} {email}\n")
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    "<html><body><h1>Registration Successful!</h1></body></html>"
                )
                self.writer.write(response.encode())
                await self.writer.drain()
            else:
                await self.send_error(400, "Bad Request: Missing username or email")
        except Exception as e:
            APP_LOGGER.error(f"Error handling registration: {e}")
            await self.send_error(500, "Internal Server Error")

    async def send_error(self, status_code, message):
        response = (
            f"HTTP/1.1 {status_code} {message}\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            f"<html><body><h1>{status_code} {message}</h1></body></html>"
        )
        self.writer.write(response.encode())
        await self.writer.drain()
        await self.writer.close()

async def main(host="localhost", port=8085):
    async def handle_client(reader, writer):
        client = HTTPServer(reader, writer)
        try:
            await client.handle_request()
        except asyncio.CancelledError:
            APP_LOGGER.info("Client connection closed.")
        except Exception as e:
            APP_LOGGER.error(f"Error handling client: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    try:
        server = await asyncio.start_server(handle_client, host, port)
        addr = server.sockets[0].getsockname()
        APP_LOGGER.info(f"Serving on {addr}")
        async with server:
            await server.serve_forever()
    except OSError as e:
        APP_LOGGER.error(f"Could not start server: {e}")

if __name__ == "__main__":
    asyncio.run(main())