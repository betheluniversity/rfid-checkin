from flask import session


class RFIDController(object):
    def __init__(self):
        pass

    # This method get's the current alert (if there is one) and then resets alert to nothing
    def get_alert(self):
        if 'alert' not in session.keys():
            session['alert'] = []
        alert_return = session['alert']
        session['alert'] = []
        return alert_return

    # This method sets the alert for when one is needed next
    def set_alert(self, message_type, message):
        session['alert'].append({
            'type': message_type,
            'message': message
        })
        session.modified = True