from datetime import datetime
from app import db
from app.model.events_schema import EventSchema
from app.lib.code_handling import EventStatus

# 根據時間自動更新EVENT.STATUS
def update_event_status():    
    curr = datetime.now()
    curr_timestamp = int(curr.timestamp())

    events = db.session.query(EventSchema).all()

    for event in events:
        if event.status == EventStatus.EVENT_CANCELED:
            continue
        if event.event_end_date < curr_timestamp:
            event.status = EventStatus.EVENT_COMPLETED

        elif event.apply_end_date and event.apply_end_date < curr_timestamp:
            event.status = EventStatus.EVENT_APPLY_END

        elif event.apply_start_date <= curr_timestamp <= (event.apply_end_date or curr_timestamp):
            event.status = EventStatus.EVENT_AVAILABLE

    db.session.commit()