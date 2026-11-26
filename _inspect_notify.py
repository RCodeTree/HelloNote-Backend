# -*- coding: utf-8 -*-
from app.db.database import SessionLocal
from app.models.notification import Notification

db = SessionLocal()
try:
    rows = db.query(Notification).order_by(Notification.id.desc()).limit(8).all()
    for n in rows:
        print(n.id, "|", n.type, "|", n.user_id, "|", n.actor_id, "|", n.related_id, "|", n.is_read, "|", n.created_at, "|", n.content)
finally:
    db.close()
