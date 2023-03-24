from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def get_token(client_id: str, client_secret: str) -> dict[str, str]:
    client = BackendApplicationClient(client_id=client_id, token_type="Bearer")
    oauth2 = OAuth2Session(client=client)
    token_url = "https://id.cisco.com/oauth2/default/v1/token"
    return oauth2.fetch_token(
        method="POST",
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        include_client_id=True,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        verify=False,
    )
