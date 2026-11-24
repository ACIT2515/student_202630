"""A minimal object-oriented client for the echo server in demo_server.py.

Start the server first:
    uv run flask --app demo_server run --debug

Then run this client in a second terminal:
    uv run python demo_client.py
"""

import httpx


class EchoClient:
    """Send JSON to the echo server and return its reply.

    Attributes:
        base_url: The address of the echo server.
    """

    def __init__(self, schema: str = "http", host: str = "localhost", port: int = 5000, path: str = ""):
        """Store the server address.

        Args:
            base_url: The address of the echo server.
        """
        self.base_url = schema + "://" + host + ":" + str(port) + "/" + path

    def echo(self, data: dict) -> dict:
        """Send data to the server and return the JSON reply.

        Args:
            data: Any JSON-compatible dict to send.

        Returns:
            dict: The echoed data with a "received_at" timestamp.
        """
        # json= encodes the dict and sets the Content-Type header.
        response = httpx.post(f"{self.base_url}/api/echo", json=data)
        # Raise an error for a 4xx or 5xx status instead of failing silently.
        response.raise_for_status()
        return response.json()


def main():
    """Send one request to the echo server and print the reply."""
    client = EchoClient("http", "localhost", 5000)
    reply = client.echo({"host": "localhost", "status": "up"})
    print(reply)


if __name__ == "__main__":
    main()
