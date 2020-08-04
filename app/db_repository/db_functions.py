from sqlalchemy.exc import DatabaseError

from app.db_repository import engine


class Banner():
    def __init__(self):
        self.engine = engine

    def _result_proxy_to_dicts(self, results):
        try:
            return_list = []
            for result in results:
                return_list.append(dict(result))
            results.close()
            return return_list
        except TypeError:
            results.close()
            return []

    def get_sessions_for_user(self, username):
        try:
            results = self.engine.execute("""
                SELECT *
                FROM BU_RFID_SCANNER_SESSIONS 
                LEFT JOIN (
                    SELECT BU_RFID_SCANNER_SCANS.session_id, COUNT(card_id) as total
                    FROM BU_RFID_SCANNER_SCANS
                    GROUP BY session_id
                ) count_table 
                ON BU_RFID_SCANNER_SESSIONS.id = count_table.session_id
                WHERE BU_RFID_SCANNER_SESSIONS.owner_username=:username AND BU_RFID_SCANNER_SESSIONS.deleted='N'
                ORDER BY BU_RFID_SCANNER_SESSIONS.ID DESC
            """, username=username)
            return self._result_proxy_to_dicts(results)
        except DatabaseError:
            return []

    def start_session(self, session_id):
        try:
            self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET status='Open'
                WHERE id=:session_id and (status='Open' or status='Archived')
            """, session_id=session_id)
            return True
        except DatabaseError:
            return False

    def close_session(self, session_id):
        try:
            self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET status='Archived'
                WHERE id=:session_id and status='Open'
            """, session_id=session_id)
            return True
        except DatabaseError:
            return False

    def delete_session(self, session_id):
        try:
            self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET deleted='Y'
                WHERE id=:session_id
            """, session_id=session_id)
            return True
        except DatabaseError:
            return False

    def create_new_session(self, username, form_name, form_description):
        try:
            # todo is this automatically closed?
            self.engine.execute("""
                INSERT INTO BU_RFID_SCANNER_SESSIONS (FORM_NAME, OWNER_USERNAME, DESCRIPTION)
                VALUES(:form_name, :username, :form_description)
            """, form_name=form_name, username=username, form_description=form_description)
            return True
        except DatabaseError:
            return False

    def edit_session(self, session_id, form_name, form_description):
        try:
            results = self.engine.execute("""
                UPDATE BU_RFID_SCANNER_SESSIONS
                SET form_name=:form_name,description=:form_description
                WHERE id=:session_id
            """, form_name=form_name, form_description=form_description, session_id=session_id)
            return True
        except DatabaseError:
            return False

    ## todo: useages?
    def scan_user(self, session_id, card_id, username=None, first_name=None, last_name=None):

        results = self.engine.execute("""
            SELECT * from BU_RFID_SCANNER_SCANS where session_id=:session_id and card_id=:card_id and SCANOUT_DATETIME IS NULL order by id desc
        """, session_id=session_id, card_id=card_id)
        rows = self._result_proxy_to_dicts(results)
        if len(rows):
            checkin_id = rows[0]['id']
            self.engine.execute("""
                                UPDATE BU_RFID_SCANNER_SCANS SET scanout_datetime=CURRENT_TIMESTAMP where id=:checkin_id
                            """, checkin_id=checkin_id)
            return 'check out'

        else:
            self.engine.execute("""
                INSERT INTO BU_RFID_SCANNER_SCANS (session_id, card_id, username, first_name, last_name, scan_datetime)
                VALUES(:session_id, :card_id, :username, :first_name, :last_name, CURRENT_TIMESTAMP)
            """, session_id=session_id, card_id=card_id, username=username, first_name=first_name, last_name=last_name)
            return 'check in'

    def get_session(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT * 
                FROM BU_RFID_SCANNER_SESSIONS 
                WHERE id=:session_id AND deleted='N'
            """, session_id=session_id)
            return self._result_proxy_to_dicts(results)[0]
        except (IndexError, DatabaseError):
            return {}

    def get_session_data_for_csv(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT scan_datetime, first_name, last_name, username, card_id
                FROM BU_RFID_SCANNER_SCANS
                WHERE session_id=:session_id
                ORDER BY scan_datetime
            """, session_id=session_id)
            return self._result_proxy_to_dicts(results)
        except DatabaseError:
            return {}

    def get_number_of_scans_for_session(self, session_id):
        try:
            results = self.engine.execute("""
                SELECT COUNT(*) 
                FROM BU_RFID_SCANNER_SCANS
                WHERE session_id=:session_id
            """, session_id=session_id)
            return self._result_proxy_to_dicts(results)[0]
        except (DatabaseError, IndexError):
            return {}

    def can_user_access_session(self, username, session_id):
        try:
            results = self.engine.execute("""
                SELECT *
                FROM BU_RFID_SCANNER_SESSIONS
                WHERE id=:session_id AND owner_username=:username
            """, session_id=session_id, username=username)
            return len(self._result_proxy_to_dicts(results)[0])
        except (IndexError, DatabaseError):
            return {}

    def get_checkins_for_session(self, session_id):
        try:
            # join on spriden and gobtpac in order to display current bethel id when needed
            results = self.engine.execute("""
                select id, completed, TO_CHAR(scan_datetime, 'MM/DD/YYYY HH:MI:SS') as scan_datetime, first_name, last_name, username, card_id, spriden_id as bethel_id, gobtpac_external_user
                from banweb.BU_RFID_SCANNER_SCANS, spriden, gobtpac
                where spriden_change_ind is null
                and spriden_pidm = gobtpac_pidm
                and gobtpac_external_user=BU_RFID_SCANNER_SCANS.username
                and SESSION_ID=:session_id
                order by scan_datetime
            """, session_id=session_id)
            return self._result_proxy_to_dicts(results)
        except DatabaseError:
            return {}

    def complete_checkin(self, checkin_id):
        self.engine.execute("""
           UPDATE BU_RFID_SCANNER_SCANS
           SET 
               completed = CASE WHEN completed = 0 then 1 else 0 end
           WHERE id=:checkin_id
        """, checkin_id=checkin_id)
        try:
            results = self.engine.execute("""
                            SELECT id, completed, scan_datetime, first_name, last_name, username, card_id
                            FROM BU_RFID_SCANNER_SCANS
                            WHERE id=:checkin_id
                        """, checkin_id=checkin_id)
            return self._result_proxy_to_dicts(results)
        except DatabaseError:
            return {}
