import re

from flask import render_template, request, session, abort, make_response, redirect, url_for
from flask import json as fjson
from flask_classy import FlaskView, route

from app import app
from app.db_repository.db_functions import Banner
from app.wsapi import WSAPIController


# TODO: create alerts
# 2 + 3 + 5
class View(FlaskView):

    def __init__(self):
        self.banner = Banner()
        self.wsapi = WSAPIController()

    def before_request(self, name, **kwargs):
        if not session.get('username', None):
            if app.config['ENVIRON'] == 'prod':
                session['username'] = request.environ.get('REMOTE_USER')
            else:
                session['username'] = app.config['TEST_USER']
        pass

    def index(self):
        rfid_sessions = self.banner.get_sessions_for_user(session.get('username'))
        return render_template('index.html', **locals())

    #todo: create the modal
    @route('/create-new-session', methods=['POST'])
    def create_new_session(self):
        rform = request.form
        form_name = rform.get('form_name')
        form_description = rform.get('form_description')
        status = self.banner.create_new_session(session.get('username'), form_name, form_description)

        if status:
            return redirect(url_for('View:index'))
        else:
            return 'failed'

    #todo: delete the session and any data with it - wait for session data to be input to make testing easier
    @route('/delete-session/<session_id>', methods=['POST'])
    def delete_session(self, session_id):
        status = self.banner.delete_session(session_id)

        if status:
            return 'success'
        else:
            return 'failed'

    #todo: Wait until create-new-session exists, to leverage the same form
    @route('/edit-session', methods=['POST'])
    def edit_session(self):
        pass

    @route('/archive-session', methods=['POST'])
    def archive_session(self):
        rform = request.form
        session_id = 1
        closed_session = self.banner.close_session(session_id)
        if not closed_session:
            return 'failed'
        return 'success'

    @route('/start-session', methods=['POST'])
    def start_session(self):
        rform = request.form
        session_id = rform.get('session_id')
        started_session = self.banner.start_session(session_id)
        if not started_session:
            return 'failed'
        return redirect(url_for('View.scan_session'))

    @route('/scan-session/<session_id>', methods=['GET'])
    def scan_session(self, session_id):
        return render_template('scan_session.html', **locals())

    # todo: write the code to pull in card_id
    @route('/scan', methods=['POST'])
    def scan(self):
        return 'success'

    @route('/no-cas/verify-scanner', methods=['post'])
    def verify_scanner(self):
        form = request.form
        scan = form.get("scan")
        session_id = form.get("session_id")
        card_id = re.search("\[\[(.+?)\]\]", scan).group(1)

        if card_id:
            # todo: clean this snippet up
            username = self.wsapi.get_user_from_prox(card_id).get('username')
            user_data = self.wsapi.get_names_from_username(username).get('0')
            if user_data.get('prefFirstName'):
                first_name = user_data.get('prefFirstName')
            else:
                first_name = user_data.get('firstName')
            last_name = user_data.get('lastName')

            self.banner.scan_user(session_id, card_id, username, first_name, last_name)
            return 'success'
        else:
            return 'failed'
