import hmac
import hashlib
import json
import logging
import os
import base64
import requests
from fastapi import APIRouter, Request, Header, HTTPException
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def verify_signature(secret, body, signature):
    """Verify GitHub webhook signature using HMAC-SHA256."""
    mac = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    expected_signature = f"sha256={mac}"
    return hmac.compare_digest(expected_signature, signature)


def decrypt_token(encrypted_token, iv):
    """Decrypt API token using WEBHOOK_SECRET as the key."""
    try:
        # Generate the key from WEBHOOK_SECRET in the same way as the GitHub Action
        key = hashlib.sha256(WEBHOOK_SECRET.encode()).hexdigest()
        key_bytes = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)
        
        # Base64 decode the encrypted token
        encrypted_data = base64.b64decode(encrypted_token)
        
        # Create cipher and decrypt
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_bytes = cipher.decrypt(encrypted_data)
        
        # Handle padding properly
        try:
            unpadded = unpad(decrypted_bytes, AES.block_size)
        except ValueError:
            # If unpadding fails, try to find the null termination
            if b'\x00' in decrypted_bytes:
                unpadded = decrypted_bytes[:decrypted_bytes.index(b'\x00')]
            else:
                unpadded = decrypted_bytes
                
        return unpadded.decode('utf-8')
    except Exception as e:
        logger.error(f"Token decryption error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to decrypt token")


def get_pr_commits(repo_full_name, pr_number, github_token):
    """Fetch the list of commits for a PR from GitHub API."""
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/commits"
    print(url)
    headers = {"Authorization": f"{github_token}", "Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch commits: {response.text}")
        raise HTTPException(status_code=500, detail="Error fetching PR commits")

    return response.json()


@router.post("/github-webhook")
async def github_webhook(
    request: Request, 
    x_hub_signature_256: str = Header(None),
    x_encrypted_token: str = Header(None, alias="X-Encrypted-Token"),
    x_token_iv: str = Header(None, alias="X-Token-IV")
):
    """Receives GitHub webhook payload and fetches PR commits if applicable."""
    body = await request.body()

    # Verify webhook signature
    if WEBHOOK_SECRET and x_hub_signature_256:
        if not verify_signature(WEBHOOK_SECRET, body, x_hub_signature_256):
            logger.error("Signature verification failed")
            raise HTTPException(status_code=403, detail="Invalid signature")

    # Validate encrypted token headers
    if not x_encrypted_token or not x_token_iv:
        logger.error("Missing encryption headers")
        raise HTTPException(status_code=403, detail="Missing token encryption headers")

    # Decrypt the token
    try:
        github_token = decrypt_token(x_encrypted_token, x_token_iv)
    except Exception as e:
        logger.error(f"Token decryption failed: {str(e)}")
        raise HTTPException(status_code=403, detail="Token decryption failed")

    payload = await request.json()
    # save this locally
    with open("samples/payload.json", "w") as f:
        json.dump(payload, f)
    event_type = payload.get("action", "")

    logger.info(f"Received GitHub event: {event_type}")
    
    if event_type == "synchronize":
        action = payload.get("action", "")
        if action in ["opened", "synchronize", "reopened"]:
            repo_full_name = payload["repository"]["full_name"]
            pr_number = payload["pull_request"]["number"]
            commits = get_pr_commits(repo_full_name, pr_number, github_token)

            logger.info(f"Fetched {len(commits)} commits for PR #{pr_number}")
            return {"message": "PR processed", "pr_number": pr_number, "commits_count": len(commits)}

    return {"message": "Webhook received", "event": event_type}