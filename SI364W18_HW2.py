## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

##Resources##
# https://www.programsinformationpeople.org/runestone/static/publicpy3/NestedData/ListswithComplexItems.html
# Lecture4Example1


#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests, json
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album:',validators=[Required()])
    rbutton = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1', '1'), ('2','2'), ('3','3')], validators=[Required()])
    submit = SubmitField('Submit')



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistinfo', methods=['GET','POST'])
def art_inf():
    for k in request.args:
        artist = "{}".format(request.args.get(k,""))
        baseurl = "https://itunes.apple.com/search"
        params = {}
        params["term"] = artist
        params["media"] = "music"
        params["entity"] = "musicTrack"
        o = requests.get(baseurl, params = params)
        d = json.loads(o.text)
        allinf= d['results']

    return render_template('artist_info.html', objects=allinf)

@app.route('/artistlinks')
def art_link():
    return render_template('artist_links.html')

@app.route('/artistform', methods=['GET', 'POST'])
def art_form():
    return render_template('artistform.html')

@app.route('/specific/song/<art_name>')
def spec_art(art_name):
    baseurl = "https://itunes.apple.com/search"
    params = {}
    params["term"] = art_name
    params["media"] = "music"
    params["entity"] = "musicTrack"
    o = requests.get(baseurl, params = params)
    d = json.loads(o.text)

    ##the following grey code was used for debugging purposes##
    #print(type(d))
    #print(d.keys())
    allinf= d['results']
    #print(type(allinf))

    return  render_template('specific_artist.html', results=allinf)

@app.route('/album_entry')
def albument():
    form = AlbumEntryForm()
    return render_template('album_entry.html', form=form)

@app.route('/album_result', methods=["GET", "POST"])
def albumres():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        album = form.album.data
        rbutton = form.rbutton.data
    return render_template('album_data.html', album=album, score=rbutton)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
