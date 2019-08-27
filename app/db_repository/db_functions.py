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
        try:
            results = self.engine.execute("""
                SELECT *
                FROM BU_RFID_SCANNER_SESSIONS 
                LEFT JOIN (
                    SELECT BU_RFID_SCANNER_SCANS.session_id, COUNT(username) as total
                    FROM BU_RFID_SCANNER_SCANS
                    GROUP BY session_id
                ) count_table 
                ON BU_RFID_SCANNER_SESSIONS.id = count_table.session_id
                WHERE BU_RFID_SCANNER_SESSIONS.owner_username='{}' AND BU_RFID_SCANNER_SESSIONS.deleted='N'
                ORDER BY BU_RFID_SCANNER_SESSIONS.ID DESC
            """.format(username))
            return self._result_proxy_to_dicts(results)
        except:
            return []

    def start_session(self, session_id):
        try:
            results = self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET status='Open'
                WHERE id='{}' and (status='Open' or status='Closed')
            """.format(session_id))
            return True
        except:
            return False

    def close_session(self, session_id):
        try:
            results = self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET status='Closed'
                WHERE id='{}' and status='Open'
            """.format(session_id))
            return True
        except:
            return False

    def delete_session(self, session_id):
        try:
            results = self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET deleted='Y'
                WHERE id='{}'
            """.format(session_id))
            return True
        except:
            return False

    def create_new_session(self, username, form_name, form_description):
        try:
            results = self.engine.execute("""
                INSERT INTO BU_RFID_SCANNER_SESSIONS (FORM_NAME, OWNER_USERNAME, DESCRIPTION)
                VALUES('{}', '{}', '{}')
            """.format(form_name, username, form_description))
            return True
        except:
            return False

    def edit_session(self, session_id, form_name, form_description):
        try:
            results = self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET form_name='{}',description='{}'
                WHERE id='{}'
            """.format(form_name, form_description, session_id))
            return True
        except:
            return False

    def scan_user(self, session_id, card_id, username, first_name, last_name):
        try:
            results = self.engine.execute("""
                INSERT INTO BU_RFID_SCANNER_SCANS (session_id, card_id, username, first_name, last_name, scan_datetime)
                VALUES({}, {}, '{}', '{}', '{}', CURRENT_TIMESTAMP)
            """.format(session_id, card_id, username, first_name, last_name))
            return True
        except:
            return False

    def get_session(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT * 
                FROM BU_RFID_SCANNER_SESSIONS 
                WHERE id={} AND deleted='N'
            """.format(session_id))
            return self._result_proxy_to_dicts(results)[0]
        except IndexError:
            return {}

    def get_session_data_for_csv(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT scan_datetime, first_name, last_name, username, card_id
                FROM BU_RFID_SCANNER_SCANS
                WHERE session_id={}
                ORDER BY scan_datetime
            """.format(session_id))
            return self._result_proxy_to_dicts(results)
        except:
            return {}

    def get_number_of_scans_for_session(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT COUNT(*) 
                FROM BU_RFID_SCANNER_SCANS
                WHERE session_id={}
            """.format(session_id))
            return self._result_proxy_to_dicts(results)[0]
        except IndexError:
            return {}

    def can_user_access_session(self, username, session_id):
        try:
            results = self.engine.execute("""
                SELECT *
                FROM BU_RFID_SCANNER_SESSIONS
                WHERE id={} AND owner_username='{}'
            """.format(session_id, username))
            return len(self._result_proxy_to_dicts(results)[0])
        except IndexError:
            return {}
