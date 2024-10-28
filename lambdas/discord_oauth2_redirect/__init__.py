import json
import logging
import os

import requests

from shared import middleware

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")


@middleware(logger)
def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    code = body.get("code", None)

    if code is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "code is required"}),
        }

    res = requests.post(
        url="https://discord.com/api/v10/oauth2/token",
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'client_id': DISCORD_CLIENT_ID,
            'client_secret': DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': "https://chzzk.junah.dev/login",
            'scope': 'identify, email, guilds'
        }
    )

    if res.status_code != 200:
        logger.error(
            json.dumps(
                {
                    "type": "INVALID_CODE",
                    "status_code": res.status_code,
                    "response": res.text
                }
            )
        )
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "code is invalid"}),
        }

    data = res.json()

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
