"""A minimal object-oriented Flask echo server.

The server accepts a JSON request, adds a timestamp, and sends the
JSON back to the client.

Run with:
    uv run flask --app demo_server run --debug

Endpoint:
    POST /api/echo  — Echo the JSON body with a "received_at" timestamp
"""

from datetime import UTC, datetime

from flask import Flask, request


class EchoServer:
    """Handle HTTP requests by echoing JSON with a timestamp.

    Attributes:
        app: The Flask application with routes bound to this object's methods.
    """

    def __init__(self):
        """Create the Flask app and register its route."""
        # __name__ is the import_name of the application package 
        # this is a single module application so set it to __name__ 
        # see https://flask.palletsprojects.com/en/stable/api/#flask.Flask
        self.app = Flask(__name__)

        # Connect the URL and HTTP method to the bound method self.echo.
        # https://flask.palletsprojects.com/en/stable/api/#flask.Flask.add_url_rule
        self.app.add_url_rule("/api/echo", view_func=self.echo, methods=["POST"])

    def echo(self):
        """Return the received JSON with a timestamp added.

        Returns:
            dict | tuple: The echoed JSON (200), or an error message (400)
                if the request body is not JSON.
        """
        # silent=True returns None instead of raising an error for bad JSON.
        data = request.get_json(silent=True)
        if data is None:
            return {"error": "Request body must be JSON"}, 400

        return {
            "received": data,
            "received_at": datetime.now(UTC).isoformat(),
        }


def create_app() -> Flask:
    """Build the application for the Flask CLI or tests.

    Returns:
        Flask: The configured application.
    """
    # Flask's --app option finds a factory named create_app automatically.
    return EchoServer().app


def main():
    """Launch the Flask development server in debug mode."""
    # Alternatively, from this folder, run:
    # uv run flask --app demo_server run --debug
    # The Flask CLI imports this module and calls create_app() instead of main().
    create_app().run(debug=True)


if __name__ == "__main__":
    main()
