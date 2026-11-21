# -*- coding: utf-8 -*-
from app.db.database import engine
from sqlalchemy import text

c = engine.connect()

def show(title, sql):
    print(f"=== {title} ===")
    rows = c.execute(text(sql)).mappings().all()
    if not rows:
        print("  (empty)")
    for r in rows:
        print("  " + str(dict(r)))

show("USERS", "SELECT id,username,display_name FROM users ORDER BY id")
show("FRIENDSHIPS", "SELECT id,requester_id,addressee_id,status,note,privacy,relation_type,closeness FROM friendships ORDER BY id")
show("CONVERSATIONS", "SELECT id,user_a_id,user_b_id,user_low_id,user_high_id FROM conversations ORDER BY id")
show("MESSAGES", "SELECT id,conversation_id,sender_id,content,is_read FROM messages ORDER BY id")
show("NOTIFICATIONS", "SELECT id,user_id,type,content,actor_id,is_read FROM notifications ORDER BY id")
show("FRIENDS OF DEMO", """SELECT f.id, f.status, f.note,
    CASE WHEN f.requester_id=1 THEN u2.username ELSE u1.username END AS peer,
    CASE WHEN f.requester_id=1 THEN f.addressee_id ELSE f.requester_id END AS peer_id
    FROM friendships f
    JOIN users u1 ON u1.id=f.requester_id
    JOIN users u2 ON u2.id=f.addressee_id
    WHERE f.requester_id=1 OR f.addressee_id=1 ORDER BY f.id""")
c.close()
