import anyio
from flask import render_template, request, flash, url_for, Blueprint
from werkzeug.utils import redirect

from database import db
from models import Link, LinkStatusCodeIn


links = Blueprint('links', __name__, template_folder='templates')


@links.route("/")
def show_all():
    return render_template('links.html', links=Link.query.all())


@links.route("/<link_id>")
def get_link_by_id(link_id):
    link = Link.query.get(link_id)
    return render_template('link.html', link=link)


@links.route('/add', methods=['GET', 'POST'])
def add_link():
    if request.method == 'POST':
        if not request.form['link']:
            flash('Please enter link field', 'error')
        else:
            link_str = request.form['link']
            link = Link(link_str, request.form['description'])
            db.session.add(link)
            db.session.commit()
            sendMessageInRabbit(link.id.__str__())
            return redirect(url_for('links.show_all'))
    return render_template('link_form.html')


from amqp import loop, send


def sendMessageInRabbit(body):
    print(' [x] Send message to SDK')

    loop.run_until_complete(send(body))
    # loop.run_until_complete(send(body, 'emoshape'))


