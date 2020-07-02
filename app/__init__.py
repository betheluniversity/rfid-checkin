from datetime import datetime

from flask import Flask, render_template, make_response, redirect, session
from flask_cors import CORS

import sentry_sdk

app = Flask(__name__)
app.config.from_object('config')
app.url_map.strict_slashes = False
CORS(app)

if app.config['SENTRY_URL']:
    from sentry_sdk.integrations.flask import FlaskIntegration
    sentry_sdk.init(dsn=app.config['SENTRY_URL'], integrations=[FlaskIntegration()])
from app.views import View
from app.controllers import RFIDController

View.register(app, route_base='/')

@app.route("/main_js")
def main_js():
    return render_template("/js/main.js")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    resp = make_response(redirect(app.config['LOGOUT_URL']))
    resp.set_cookie('MOD_AUTH_CAS_S', '', expires=0, path='/')
    resp.set_cookie('MOD_AUTH_CAS', '', expires=0, path='/')
    return resp


@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicons/favicon.ico')


# This makes these variables open to use everywhere
@app.context_processor
def utility_processor():
    to_return = {}
    to_return.update({
        'alert': RFIDController().get_alert(),
        'now': datetime.now()
    })

    return to_return


def datetimeformat(value, custom_format=None):
    if value:
        if custom_format:
            return value.strftime(custom_format)

        if value.strftime('%l:%M:%p') == '12:00AM':  # Check for midnight
            return 'midnight'

        if value.strftime('%l:%M:%p') == '12:00PM':  # Check for noon
            return 'noon'

        if value.strftime('%M') == '00':
            time = value.strftime('%l')
        else:
            time = value.strftime('%l:%M')

        if value.strftime('%p') == 'PM':
            time = '{0} {1}'.format(time, 'p.m.')
        else:
            time = '{0} {1}'.format(time, 'a.m.')

        return time

    else:
        return '???'


app.jinja_env.filters['datetimeformat'] = datetimeformat