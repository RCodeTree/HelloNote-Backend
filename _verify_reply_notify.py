# -*- coding: utf-8 -*-
"""端到端验证：评论被回复时生成 reply 通知"""
import json
import urllib.request

BASE = "http://127.0.0.1:8000/api/v1"


def call(method, path, token=None, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else None


def login(account, password):
    return call("POST", "/auth/login", body={"account": account, "password": password})["access_token"]


t_demo = login("demo", "demo1234")
t_b = login("penpal_b", "test123456")

# demo 建笔记 + 发评论
note = call("POST", "/notes", t_demo, {"title": "回复通知测试", "content": "验证回复通知", "format": "text", "is_public": False, "tag_ids": []})
comment = call("POST", f"/comments/notes/{note['id']}/comments", t_demo, {"content": "demo 的原始评论"})

# penpal_b 回复 demo 的评论
reply = call("POST", f"/comments/notes/{note['id']}/comments", t_b, {"content": "回复 demo 的评论", "parent_id": comment["id"]})

# demo 拉取通知
notifs = call("GET", "/notifications", t_demo)
replies = [n for n in notifs if n["type"] == "reply"]

print(json.dumps({
    "noteId": note["id"],
    "commentId": comment["id"],
    "replyId": reply["id"],
    "replyParentId": reply["parent_id"],
    "replyCount": len(replies),
    "replies": [{"id": n["id"], "actor": n["actor_name"], "content": n["content"], "related": n["related_id"]} for n in replies[:5]],
}, ensure_ascii=False))
