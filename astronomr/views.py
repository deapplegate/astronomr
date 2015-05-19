import sqlite3
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from astronomr import app, db, model, forms





###########
###  Views

@app.route('/object/<int:object_id>')
def show_object(object_id):
    
    theobject = model.Object.query.get(object_id)
    if theobject is None:
        abort(404)

    observations = theobject.logged_observations.order_by(model.LoggedObservation.id.desc())[:10]
    
    return render_template('show_object.html', theobject = theobject,
                           observations = observations)

###

@app.route('/object/<int:object_id>/edit', methods=['GET','POST'])
def edit_object(object_id):

    if not session.get('logged_in'):
        abort(401)

    theobject = model.Object.query.get(object_id)
    if theobject is None:
        abort(404)

    edit_object_form = forms.EditObjectForm(obj = theobject)
    if edit_object_form.validate_on_submit():

        theobject.name = edit_object_form.name.data
        theobject.text = edit_object_form.text.data

        db.session.add(theobject)
        db.session.commit()

        flash('%s successfully updated' % theobject.name)
        return redirect(url_for('show_object', object_id = object_id))

    

    return render_template('edit_object.html', theobject = theobject,
                           edit_object_form = edit_object_form)

        

###

def get_newest_obs(nobs):

    observations = model.LoggedObservation.query.order_by(model.LoggedObservation.id.desc())[:nobs]

    return observations

###


@app.route('/')
@app.route('/add', methods=['GET', 'POST'])
def show_observations():

    new_obs_interface = do_add_observation()

    newest_obs = get_newest_obs(10)

    return render_template('show_entries.html', new_obs_interface = new_obs_interface, observations=newest_obs)



###

def do_add_observation():
        
    if not session.get('logged_in'):
        return ''

    new_obs_form = forms.LoggedObservationForm()
    if new_obs_form.validate_on_submit():

        new_obs = model.LoggedObservation(title = new_obs_form.title.data,
                                          timestamp = new_obs_form.timestamp.data,
                                          description = new_obs_form.description.data)
        db.session.add(new_obs)

        object_names = new_obs_form.objects.data.split(',')
        for object_name in object_names:
            theobject = model.Object.query.filter_by(name = object_name).first()
            if theobject is None:
                theobject = model.Object(name=object_name, text='')
            new_obs.objects.append(theobject)
            db.session.add(theobject)

        db.session.commit()

        flash('New entry was successfully posted')


    return render_template('add_observation.html', new_obs_form = new_obs_form)
    
###
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_observations'))
    return render_template('login.html', error=error)

###

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_observations'))
