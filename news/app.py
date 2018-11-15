#!usr/env/bin python
# -*- coding:utf-8 -*-
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app =Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer,primary_key=True,autoincrement= True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column (db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref='categorys')
    content = db.Column(db.Text)

    def __init__(self,title,create_time,category,content):
        self.title=title
        self.create_time= create_time
        self.category= category
        self.content=content

    def __repr__(self):
        return '<File(name=%r)>' % self.title
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(80)) 
    
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<Category(name=%r)>' % self.name 

if __name__ == '__main__':
    db.create_all()
      


@app.route('/')
def index():
    l= File.query.all()
    return render_template('index.html',files=l)

@app.route('/file/<file_id>')
def file(file_id):
    f = File.query.get_or_404(file_id)
    return render_template('file.html', file=f)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

