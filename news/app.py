#!usr/env/bin python
# -*- coding:utf-8 -*-
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db1 = client.shiyanlou


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

    def add_tag(self,tag_name):
        file_tag = db1.tag.find_one({'content_id':self.id})
        if file_tag:
            tags=file_tag['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            db1.tag.update_one({'content_id':self.id},{'$set':{'tags':tags}})
        else:
            tags=[tag_name]
            db1.tag.insert_one({'content_id':self.id,'tags':tags})
        return tags


    def remove_tag(self, tag_name):
        file_tag = db1.tag.find_one({'content_id':self.id})
        if file_tag:
            tags=file_tag['tags']
            if tag_name not in tags:
                return tags
            else:
                tags= tags.remove(tag_name)
                db1.tag.update({'content_id':self.id},{'$set',{'tags':tags}})
                return tags
        return []

    @property
    def tags(self):
        file_tag = db1.tag.find_one({'content_id':self.id})
        if file_tag:
            return file_tag['tags']
        else:
            return []

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(80)) 
    
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<Category(name=%r)>' % self.name 


def insert_datas():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')

    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

if __name__ == '__main__':
    app.run()
    


      


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




