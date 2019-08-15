from app.db_repository import engine


class Banner():
    def __init__(self):
        self.engine = engine

    def _result_proxy_to_dicts(self, results):
        return_list = []
        for result in results:
            return_list.append(dict(result))
        return return_list

    def get_sessions_for_user(self, username):
        # todo: add try/except
        # todo: if user is admin, return all? or just create a separate one
        results = self.engine.execute("""
            SELECT * 
            FROM BU_RFID_SCANNER_SESSIONS 
            WHERE owner_username='{}' and deleted='N'
        """.format(username))
        return self._result_proxy_to_dicts(results)

    def start_session(self, session_id):
        results = self.engine.execute("""
            UPDATE BU_RFID_SCANNER_SESSIONS
            SET STATUS='Open'
            WHERE id='{}' and (STATUS='Created' or STATUS='Closed')
        """.format(session_id))
        return True

    def close_session(self, session_id):
        results = self.engine.execute("""
            UPDATE BU_RFID_SCANNER_SESSIONS
            SET STATUS='Closed'
            WHERE id='{}' and STATUS='Open'
        """.format(session_id))
        return True

    def delete_session(self, session_id):
        results = self.engine.execute("""
            UPDATE BU_RFID_SCANNER_SESSIONS
            SET DELETED='Y'
            WHERE id='{}'
        """.format(session_id))
        return True

    def create_new_session(self, username, form_name, form_description):
        results = self.engine.execute("""
            INSERT INTO BU_RFID_SCANNER_SESSIONS (FORM_NAME, OWNER_USERNAME, DESCRIPTION)
            VALUES('{}', '{}', '{}')
        """.format(form_name, username, form_description))
        return True

    def edit_session(self, session_id, form_name, form_description):
        results = self.engine.execute("""
            UPDATE BU_RFID_SCANNER_SESSIONS
            SET FORM_NAME='{}',DESCRIPTION='{}'
            WHERE id='{}'
        """.format(form_name, form_description, session_id))
        return True

    def scan_user(self, session_id, card_id, username, first_name, last_name):
        results = self.engine.execute("""
            INSERT INTO BU_RFID_SCANNER_SCANS (SESSION_ID, CARD_ID, USERNAME, FIRST_NAME, LAST_NAME, SCAN_DATETIME)
            VALUES({}, {}, '{}', '{}', '{}', CURRENT_TIMESTAMP)
        """.format(session_id, card_id, username, first_name, last_name))
        return True

    def get_session(self, session_id):
        results = self.engine.execute("""
            SELECT * 
            FROM BU_RFID_SCANNER_SESSIONS 
            WHERE ID={} AND DELETED='N'
        """.format(session_id))
        return self._result_proxy_to_dicts(results)[0]

    def get_session_data_for_csv(self, session_id):
        results = self.engine.execute("""
            SELECT SCAN_DATETIME, FIRST_NAME, LAST_NAME, USERNAME, CARD_ID
            FROM BU_RFID_SCANNER_SCANS
            WHERE SESSION_ID={}
            ORDER BY SCAN_DATETIME
        """.format(session_id))
        return self._result_proxy_to_dicts(results)

    