from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Message, User, Group
from . import db   ##means from __init__.py import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        pass 

    if request.method == 'POST':
        pass
    return render_template('index.html', user=current_user)


@views.route('/delete-mess', methods=['POST'])
def delete_mess():
    mess = json.loads(request.data)
    messId = mess['mId']
    print(messId)
    mess = Message.query.get(messId)
    if mess:
        if mess.user_id == current_user.id:
            db.session.delete(mess)
            db.session.commit()
    return jsonify({})

@views.route('/chat', methods=['POST'])
@login_required
def chat():
    d = request.form.get('group_code')
    print(d)
    s = '/chat/' + str(d)
    return redirect(s)
'''
@views.route('/chat/<code>', methods=['GET', 'POST'])
def solve(code):
    if request.method == 'POST':
        mess = request.form.get('message')
        sender_name = User.query.get(current_user.id)
        #g_id = Group.query.filter_by(code=code).first().id
#        new_message  = Message(name=sender_name, data=mess, user_id=current_user.id, group_id=g_id)
        print(sender_name)
        print(mess)
        print("g_id: " + str(code))
        print("u_id: " + str(current_user.id))

    group = Group.query.filter_by(code=code).first()
    name = group.name
    messages = list(group.messages)
    messages.reverse()
    print(messages)
    return render_template('chat.html', messages=messages, user=current_user, name=name, code=code)
'''

@views.route('/chat/<code>', methods=['GET', 'POST'])
@login_required
def solve(code):
    if request.method == 'POST':
        mess = request.form.get('message')
        sender_name = User.query.get(current_user.id).name
        g_id = Group.query.filter_by(code=code).first().id
        new_message  = Message(name=sender_name, data=mess, user_id=current_user.id, group_id=g_id)
        db.session.add(new_message)
        db.session.commit()

    group = Group.query.filter_by(code=code).first()
    if group!=None:
        name = group.name
        messages = list(group.messages)
        messages.reverse()

    else:
        name = 'test'
        messages=[]
    return render_template('chat.html', messages=messages, user=current_user, name=name, code=code)

@views.route('/make-group', methods=['POST'])
@login_required
def make_group():
    name = request.form.get('name')
    code = request.form.get('code')
    if len(code)<5 or len(name)<5:
        flash('Group name and code must be atleast 5 characters long!', category='error')
    q = Group.query.filter_by(code=code)
    if len(list(q))>0:
        flash('The Group code you entered already exists!', category='error')
    new_group = Group(name=name, code=code, owner_id=current_user.id)
    db.session.add(new_group)
    db.session.commit()
    flash("The Group chat is created. Join using code!")
    return redirect(url_for('views.index'))
'''
    else:
        id = current_user.id
        fet = User.query.get(id)
        for i in list(fet.notes):
            print(i.data + " " + str(i.date))
'''
'''@views.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        pass
#, messages=messages, user=current_user
    messages = list(Message.query)
    messages.reverse()
    return render_template('chat.html', messages=messages, user=current_user)'''