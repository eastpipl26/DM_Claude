# -*- coding: utf-8 -*-
"""부동산 파이프라인 공통 모듈 — config.md 경로 파싱 + API 키 로드.

경로는 config.md에서 읽는다 (하드코딩 금지 규칙).
"""
import os
import re

CLAUDE_HOME = os.path.join(os.environ["USERPROFILE"], ".claude")
CONFIG_MD = os.path.join(CLAUDE_HOME, "config.md")


def load_config():
    """config.md의 | `변수` | `값` | 표를 dict로 파싱하고 {vault}/{claude_home} 치환."""
    cfg = {}
    with open(CONFIG_MD, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", line)
            if m:
                cfg[m.group(1)] = m.group(2)
    for _ in range(3):  # 중첩 치환 해소
        for k, v in cfg.items():
            cfg[k] = v.replace("{vault}", cfg.get("vault", "")).replace(
                "{claude_home}", cfg.get("claude_home", ""))
    return cfg


def get_api_key():
    """secrets/molit.env에서 MOLIT_API_KEY 로드. 없으면 None."""
    env_path = os.path.join(CLAUDE_HOME, "secrets", "molit.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("MOLIT_API_KEY="):
                key = line.strip().split("=", 1)[1].strip()
                return key or None
    return None
