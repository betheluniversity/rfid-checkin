import csv
from datetime import datetime
from io import StringIO
import re

from flask import render_template, request, session, redirect, url_for, Response, stream_with_context
from flask_classy import FlaskView, route

from app import app
from app.db_repository.db_functions import Banner
from app.wsapi import WSAPIController


# TODO: create alerts
# 2 + 3 + 5 + 3 + 3
class View(FlaskView):

    def __init__(self):
        self.banner = Banner()
        self.wsapi = WSAPIController()

    # todo: add in aborts if you aren't the correct user. Maybe consider making it a wrapper?
    def before_request(self, name, **kwargs):
        # todo: get name and photo

        if not session.get('username', None):
            if app.config['ENVIRON'] == 'prod':
                session['username'] = request.environ.get('REMOTE_USER')
            else:
                session['username'] = app.config['TEST_USER']

        if not session.get('name', None):
            session['name'] = self.wsapi.get_names_from_username(session.get('username'))

    def index(self):
        rfid_sessions = self.banner.get_sessions_for_user(session.get('username'))
        return render_template('index.html', **locals())

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
            return redirect(url_for('View:index'))
        else:
            return 'failed'

    @route('/delete-session', methods=['POST'])
    def delete_session(self):
        rform = request.form
        session_id = rform.get('session_id')

        # Currently, we don't delete sessions, we just mark them as "deleted" and then don't display them.
        status = self.banner.delete_session(session_id)

        if status:
            return redirect(url_for('View:index'))
        else:
            return 'failed'

    @route('/close-session/<session_id>', methods=['GET'])
    def close_session(self, session_id):
        closed_session = self.banner.close_session(session_id)
        if closed_session:
            return redirect(url_for('View:index'))
        return 'failed'

    # this also does the reopen session
    @route('/start-session/<session_id>', methods=['GET'])
    def start_session(self, session_id):
        started_session = self.banner.start_session(session_id)
        if not started_session:
            return 'failed'
        # todo: we might consider not going to the session immediately when it starts. This is confusing
        return redirect(url_for('View:scan_session', session_id=session_id))

    @route('/scan-session/<session_id>', methods=['GET'])
    def scan_session(self, session_id):
        rfid_session = self.banner.get_session(session_id)
        return render_template('scan_session.html', **locals())

    @route('/no-cas/verify-scanner', methods=['post'])
    def verify_scanner(self):
        form = request.form
        scan = form.get("scan")
        session_id = form.get("session_id")
        card_id = re.search("\[\[(.+?)\]\]", scan).group(1)

        if card_id:
            # todo: clean this snippet up
            username = self.wsapi.get_user_from_prox(card_id).get('username')
            user_data = self.wsapi.get_names_from_username(username)
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')

            self.banner.scan_user(session_id, card_id, username, first_name, last_name)
            return 'success'
        else:
            return 'failed'


    @route('/download-csv/<session_id>', methods=['get'])
    def download_csv(self, session_id):
        session = self.banner.get_session(session_id)
        session_data = self.banner.get_session_data_for_csv(session_id)

        session_name = '{} {}'.format(session.get('form_name'), datetime.now().strftime('%m/%d/%Y'))
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
