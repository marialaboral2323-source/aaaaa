#!/usr/bin/env python3
import json
import sys
from typing import Tuple

import requests

BASE_URL = "https://snake2.challs.m0lecon.it"


def start_game(session: requests.Session) -> Tuple[str, dict]:
    resp = session.post(f"{BASE_URL}/api/game/start", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Game start failed: {data}")
    return data["playerId"], data["food"]


def farm_token(session: requests.Session, player_id: str) -> Tuple[str, int]:
    score_token = None
    score = 0
    for _ in range(20):
        payload = {"playerId": player_id}
        if score_token:
            payload["scoreToken"] = score_token
        resp = session.post(f"{BASE_URL}/api/game/food", json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("success"):
            raise RuntimeError(f"Food endpoint error: {data}")
        score_token = data["scoreToken"]
        score = data.get("score", 0)
        if data.get("snake_sleeping"):
            break
    else:
        raise RuntimeError("Snake never went to sleep")
    if score != 100:
        raise RuntimeError(f"Unexpected score {score}, expected 100")
    return score_token, score


def forge_token(original_token_hex: str, original_score: int, forged_score: int, player_id: str) -> str:
    token_bytes = bytes.fromhex(original_token_hex)
    nonce = token_bytes[:8]
    ciphertext = token_bytes[8:]

    original_plaintext = json.dumps({"score": original_score, "playerId": player_id})
    target_plaintext = json.dumps({"score": forged_score, "playerId": player_id})

    original_bytes = original_plaintext.encode()
    target_bytes = target_plaintext.encode()

    if len(original_bytes) != len(ciphertext):
        raise RuntimeError("Plaintext/ciphertext length mismatch")
    if len(original_bytes) != len(target_bytes):
        raise RuntimeError("Target plaintext length mismatch")

    keystream = bytes(c ^ p for c, p in zip(ciphertext, original_bytes))
    forged_ciphertext = bytes(k ^ t for k, t in zip(keystream, target_bytes))

    forged_token = nonce + forged_ciphertext
    return forged_token.hex()


def submit_score(session: requests.Session, score_token: str, name: str = "speedrunner") -> dict:
    payload = {"scoreToken": score_token, "playerName": name}
    resp = session.post(f"{BASE_URL}/api/submit-score", json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()


def main():
    session = requests.Session()
    player_id, food = start_game(session)
    print(f"Started game with player_id={player_id}, initial_food={food}")

    token_100, score = farm_token(session, player_id)
    print(f"Got token for score {score}: {token_100[:32]}...")

    forged_token = forge_token(token_100, score, 999, player_id)
    print("Forged token:", forged_token[:32], "...")

    result = submit_score(session, forged_token)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[!] Error: {exc}")
        sys.exit(1)
