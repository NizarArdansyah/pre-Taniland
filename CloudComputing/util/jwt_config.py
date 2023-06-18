from flask import jsonify
from flask_jwt_extended import JWTManager
from util.blocklist import BLOCKLIST

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "message": "Token expired",
                "error": True,
                "data": None,
            }
        ),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {
                "message": "Invalid token",
                "error": True,
                "data": None,
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


def init_app(app):
    # Menginisialisasi JWTManager dengan aplikasi Flask
    jwt.init_app(app)
