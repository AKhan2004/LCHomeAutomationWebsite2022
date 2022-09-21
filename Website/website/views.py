from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import datetime
import pyrebase

# Firebase Database (Online)
firebaseConfig = {
    "apiKey": "AIzaSyAkD-Ehz2IOwx4iA3jL_dZPpzog3vaaY94",
    "authDomain": "home-automation-794c1.firebaseapp.com",
    "databaseURL": "https://home-automation-794c1-default-rtdb.firebaseio.com",
    "projectId": "home-automation-794c1",
    "storageBucket": "home-automation-794c1.appspot.com",
    "messagingSenderId": "204270994860",
    "appId": "1:204270994860:web:2372c400f7c7f0cd272609"
}

firebase = pyrebase.initialize_app(firebaseConfig)
fb_db = firebase.database()

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/features')
def features():
    return render_template('features.html', user=current_user)


@views.route('/pricing')
def pricing():
    return render_template('pricing.html', user=current_user)


@views.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)


@views.route('/about-us')
def about_us():
    return render_template('about-us.html', user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        if request.form['submit'] == 'add_input':
            if request.form.get('command') != '':
                command = request.form.get('command')
                now = int(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))

                # Post to /command
                voice_input = {
                    'Input': command,
                    'Time': now,
                }
                fb_db.child('/command').push(voice_input)

                # Post to /virtual_assistant/voice_log
                voice_output = {
                    'Output': 'Person: ' + command,
                    'Time': now,
                }
                fb_db.child('/virtual_assistant/voice_log').push(voice_output)

                # Update database
                voice_data = fb_db.child('/virtual_assistant/voice_log').get()
                voice_data = voice_data.val()

                return redirect(url_for('views.profile'))

        elif request.form['submit'] == 'add_todo':
            if request.form.get('task') != '':
                to_do = request.form.get('task')
                to_do_dict = {
                    'To Do': to_do,
                }
                fb_db.child('/to-do').push(to_do_dict)

                to_do_list = fb_db.child('/to-do').get()
                to_do_list = to_do_list.val()

            return redirect(url_for('views.profile'))

        elif request.form['submit'] == 'delete_input':
            fb_db.child('/virtual_assistant/voice_log').remove()

        elif request.form['submit'] == 'delete_todo':
            fb_db.child('/to-do').remove()

        return redirect(url_for('views.profile'))

    # Initialise Voice Log Data
    voice_data = fb_db.child('/virtual_assistant/voice_log').get()
    voice_data = voice_data.val()

    to_do_list = fb_db.child('/to-do').get()
    to_do_list = to_do_list.val()

    # Check if database is empty
    if voice_data == None:
        if to_do_list == None:
            return render_template('profile.html', user=current_user)
        else:
            return render_template('profile.html', user=current_user, task=to_do_list.values())
    else:
        if to_do_list == None:
            return render_template('profile.html', user=current_user, log=voice_data.values())
        else:
            return render_template('profile.html', user=current_user, log=voice_data.values(), task=to_do_list.values())
