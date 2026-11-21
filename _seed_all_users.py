# -*- coding: utf-8 -*-
"""为所有可登录账号幂等补齐笔友关系/会话/通知，确保任意账号登录都有数据可验证。"""
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
now = datetime.now()


def q(sql, params=None):
    return db.execute(text(sql), params or {})


def uid(username):
    return q("SELECT id FROM users WHERE username=:u", {"u": username}).scalar()


def ensure_friendship(a, b, note, rel, close, privacy):
    lo, hi = min(a, b), max(a, b)
    row = q("SELECT id FROM friendships WHERE requester_id=:l AND addressee_id=:h",
            {"l": lo, "h": hi}).scalar()
    if row:
        q("UPDATE friendships SET status='accepted',note=:n,relation_type=:r,closeness=:c,privacy=:p WHERE id=:id",
          {"n": note, "r": rel, "c": close, "p": privacy, "id": row})
    else:
        q("INSERT INTO friendships(requester_id,addressee_id,status,note,privacy,relation_type,closeness,created_at,updated_at) "
          "VALUES(:l,:h,'accepted',:n,:p,:r,:c,:t,:t)",
          {"l": lo, "h": hi, "n": note, "p": privacy, "r": rel, "c": close, "t": now})
    db.commit()


def ensure_conv(a, b):
    lo, hi = min(a, b), max(a, b)
    cid = q("SELECT id FROM conversations WHERE user_low_id=:l AND user_high_id=:h",
            {"l": lo, "h": hi}).scalar()
    if cid:
        return cid
    q("INSERT INTO conversations(user_a_id,user_b_id,user_low_id,user_high_id,created_at,updated_at) "
      "VALUES(:l,:h,:l,:h,:t,:t)", {"l": lo, "h": hi, "t": now})
    db.commit()
    return q("SELECT id FROM conversations WHERE user_low_id=:l AND user_high_id=:h",
             {"l": lo, "h": hi}).scalar()


def add_msg(cid, sender, content, unread=True, offset=0):
    if q("SELECT id FROM messages WHERE conversation_id=:c AND sender_id=:s AND content=:m",
         {"c": cid, "s": sender, "m": content}).scalar():
        return
    q("INSERT INTO messages(conversation_id,sender_id,content,is_read,created_at) VALUES(:c,:s,:m,:r,:t)",
      {"c": cid, "s": sender, "m": content, "r": 0 if unread else 1,
       "t": now - timedelta(minutes=20 - offset * 5)})
    db.commit()
    q("UPDATE conversations SET updated_at=:t WHERE id=:c", {"t": now, "c": cid})
    db.commit()


def ensure_notice(user, ntype, content, actor=None):
    if q("SELECT id FROM notifications WHERE user_id=:u AND type=:t AND content=:c",
         {"u": user, "t": ntype, "c": content}).scalar():
        return
    q("INSERT INTO notifications(user_id,type,actor_id,content,is_read,created_at) VALUES(:u,:t,:a,:c,0,:n)",
      {"u": user, "t": ntype, "a": actor, "c": content, "n": now})
    db.commit()


demo = uid("demo")
penpal_b = uid("penpal_b")
newcomer = uid("newcomer")
rong = uid("rong")
bookworm = uid("bookworm")
traveler = uid("traveler")
coder = uid("coder")

# rong 账号：4 个笔友
for peer, note, rel, close, privacy in [
    (demo, "演示用户", "同好", "friend", "all"),
    (penpal_b, "笔友B", "笔友", "acquaintance", "friends"),
    (bookworm, "小林", "书友", "close", "all"),
    (coder, "阿杰", "代码同好", "friend", "friends"),
]:
    ensure_friendship(rong, peer, note, rel, close, privacy)

# penpal_b：3 个笔友
for peer, note in [(demo, "演示用户"), (newcomer, "新朋友"), (traveler, "阿行")]:
    ensure_friendship(penpal_b, peer, note, "笔友", "friend", "all")

# newcomer：3 个笔友
for peer, note in [(demo, "演示用户"), (penpal_b, "笔友B"), (bookworm, "小林")]:
    ensure_friendship(newcomer, peer, note, "笔友", "friend", "all")

# rong 的会话 + 未读消息
for peer, msgs in [
    (demo, ["rong 的测试消息一", "rong 的测试消息二"]),
    (bookworm, ["阿杰向你分享了一篇文章"]),
]:
    cid = ensure_conv(rong, peer)
    for i, m in enumerate(msgs):
        add_msg(cid, peer, m, unread=True, offset=i)

# 各账号通知
for user, items in [
    (rong, [("system", "欢迎使用 Hello!Note"),
            ("comment", "演示用户评论了你的笔记：写得不错"),
            ("friend_request", "书虫小林申请添加你为笔友", bookworm)]),
    (penpal_b, [("system", "欢迎使用 Hello!Note"),
                ("friend_accept", "演示用户接受了你的笔友申请", demo)]),
    (newcomer, [("system", "欢迎使用 Hello!Note")]),
]:
    for item in items:
        ensure_notice(user, item[0], item[1], item[2] if len(item) > 2 else None)

print("ALL USERS SEEDED")
for u in [demo, rong, penpal_b, newcomer]:
    name = q("SELECT username FROM users WHERE id=:i", {"i": u}).scalar()
    fc = q("SELECT COUNT(*) FROM friendships WHERE status='accepted' AND (requester_id=:i OR addressee_id=:i)", {"i": u}).scalar()
    nc = q("SELECT COUNT(*) FROM notifications WHERE user_id=:i", {"i": u}).scalar()
    print(f"  {name}: friends={fc}, notices={nc}")
db.close()
