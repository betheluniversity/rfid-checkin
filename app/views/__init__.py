import csv
from datetime import datetime
from io import StringIO
import re

from flask import session, render_template, request, redirect, url_for, Response, stream_with_context, abort, make_response
from flask_classy import FlaskView, route

from app import app
from app.controllers import RFIDController
from app.db_repository.db_functions import Banner
from app.wsapi import WSAPIController


class View(FlaskView):

    def __init__(self):
        self.banner = Banner()
        self.wsapi = WSAPIController()
        self.controller = RFIDController()

    def before_request(self, name, **kwargs):
        if '/static/' not in request.url and '/main_js' not in request.url and '/favicon.favicons' not in request.url and '/no-cas/' not in request.url:
            if 'username' not in session.keys():
                if app.config['ENVIRON'] == 'prod':
                    session['username'] = request.environ.get('REMOTE_USER')
                else:
                    session['username'] = app.config['TEST_USER']

            if 'name' not in session.keys():
                session['name'] = self.wsapi.get_names_from_username(session.get('username'))

        if 'alert' not in session.keys():
            session['alert'] = []

    def index(self):
        rfid_sessions = self.banner.get_sessions_for_user(session.get('username'))

        open_rfid_sessions = []
        archived_rfid_sessions = []
        for rfid_session in rfid_sessions:
            if rfid_session.get('status') == 'Open':
                open_rfid_sessions.append(rfid_session)
            elif rfid_session.get('status') == 'Archived':
                archived_rfid_sessions.append(rfid_session)

        return render_template('index.html', **locals())

    # this also accepts edits
    @route('/create-new-session/', methods=['POST'])
    def create_new_session(self):
        rform = request.form
        session_id = rform.get('session_id')
        form_name = rform.get('form_name')
        form_description = rform.get('form_description')

        if session_id:
            # edit
            status = self.banner.edit_session(session_id, form_name, form_description)
        else:
            # create new
            status = self.banner.create_new_session(session.get('username'), form_name, form_description)

        if status:
            if session_id:
                # successful edit message
                self.controller.set_alert('success', 'Successfully edited the session, {}.'.format(form_name))
            else:
                # successful new message
                self.controller.set_alert('success', 'Successfully created the session, {}.'.format(form_name))
        else:
            self.controller.set_alert('danger', 'ERROR: Failed to create the session, {}.'.format(form_name))

        # rfid_sessions = self.banner.get_sessions_for_user(session.get('username'))
        # return render_template('index.html', **locals())
        return redirect(url_for('View:index'))

    @route('/delete-session', methods=['POST'])
    def delete_session(self):
        rform = request.form
        session_id = rform.get('session_id')

        # permissions check
        if not self.banner.can_user_access_session(session.get('username'), session_id):
            return abort(403)

        # Currently, we don't delete sessions, we just mark them as "deleted" and then don't display them.
        status = self.banner.delete_session(session_id)

        if status:
            self.controller.set_alert('warning', 'Succesfully deleted the session')
        else:
            self.controller.set_alert('danger', 'ERROR: Failed to delete the session.')
        return redirect(url_for('View:index'))

    @route('/archive-session/<session_id>', methods=['GET'])
    def archive_session(self, session_id):

        # permissions check
        if not self.banner.can_user_access_session(session.get('username'), session_id):
            return abort(403)

        archived_session = self.banner.close_session(session_id)
        if archived_session:
            self.controller.set_alert('success', 'Succesfully archived the session')
            return redirect(url_for('View:index'))
        else:
            self.controller.set_alert('danger', 'ERROR: Failed to archived the session')
            return 'failed'

    # this also does the reopen session
    @route('/start-session/<session_id>', methods=['GET'])
    def start_session(self, session_id):

        # permissions check
        if not self.banner.can_user_access_session(session.get('username'), session_id):
            return abort(403)

        started_session = self.banner.start_session(session_id)
        if started_session:
            return redirect(url_for('View:index'))
        else:
            self.controller.set_alert('danger', 'ERROR: Failed to start the session')
            return 'failed'

    @route('/go-to-session/<session_id>', methods=['GET'])
    def go_to_session(self, session_id):
        if app.config.get('ENVIRON') == 'prod':
            session.clear()
            resp = make_response(redirect(app.config['LOGOUT_URL'] + '?service=' + request.host_url[:-1] + url_for('View:scan_session', session_id=session_id)))
            resp.set_cookie('MOD_AUTH_CAS_S', '', expires=0, path='/')
            resp.set_cookie('MOD_AUTH_CAS', '', expires=0, path='/')
            return resp
        else:
            return redirect(url_for('View:scan_session', session_id=session_id))

    @route('/no-cas/scan-session/<session_id>', methods=['GET'])
    def scan_session(self, session_id):
        rfid_session = self.banner.get_session(session_id)
        if not rfid_session:
            return abort(403)
        return render_template('scan_session.html', **locals())

    @route('/no-cas/verify-scanner', methods=['post'])
    def verify_scanner(self):
        form = request.form
        scan = form.get("scan")
        session_id = form.get("session_id")
        card_data = re.search("\[\[(.+?)\]\]", scan)

        alert_type = 'danger'
        if card_data:
            try:
                card_id = card_data.group(1)
                username = self.wsapi.get_user_from_prox(card_id).get('username')
                user_data = self.wsapi.get_names_from_username(username)
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')

                self.banner.scan_user(session_id, card_id, username, first_name, last_name)
                alert_type = 'success'
                alert_message = 'Thank you for signing in, {} {}.'.format(first_name, last_name)
            except:
                alert_message = 'ERROR: Failed sign in the user with Card ID, {}'.format(card_id)
        else:
            alert_message = 'ERROR: Failed to get the card ID. Please try again.'

        return render_template('scan_alert.html', **locals())


    @route('/download-csv/<session_id>', methods=['get'])
    def download_csv(self, session_id):

        # permissions check
        if not self.banner.can_user_access_session(session.get('username'), session_id):
            return abort(403)

        scan_session = self.banner.get_session(session_id)
        session_data = self.banner.get_session_data_for_csv(session_id)

        session_name = '{} {}'.format(scan_session.get('form_name'), datetime.now().strftime('%m/%d/%Y'))
        return self._export_csv(session_data, session_name)

    def _export_csv(self, data, csv_name):
        def generate():
            w = StringIO()
            filewriter = csv.writer(w)

            # get column names and format them
            data_to_write = []
            for key in data[0].keys():
                data_to_write.append(key.replace('_', ' ').title())
            filewriter.writerow(data_to_write)

            # write each row
            for row in data:
                new_row = row.values()

                filewriter.writerow(new_row)
                yield w.getvalue()
                w.seek(0)
                w.truncate(0)

        return Response(
            stream_with_context(generate()),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=" + csv_name + '.csv'}
        )
