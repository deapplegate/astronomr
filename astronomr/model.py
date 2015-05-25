from astronomr import db

#####

objects_observed = db.Table('objects_observed',
        db.Column('logged_observation_id', db.Integer, 
                  db.ForeignKey('logged_observation.id')),
        db.Column('object_id', db.Integer, db.ForeignKey('object.id')))
                            

####

class LoggedObservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.Text)
    objects = db.relationship('Object', secondary=objects_observed,
                              backref=db.backref('logged_observations', 
                                                 lazy='dynamic'))


    def __repr__(self):
        return '<LoggedObservation %r: %r>' % (self.id, self.title)
    
#####

class Object(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True)
    text = db.Column(db.Text)
    #backref: logged_observations (dynamic)

    def __repr__(self):
        return '<Object %r: %r>' % (self.id, self.name)

######

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

