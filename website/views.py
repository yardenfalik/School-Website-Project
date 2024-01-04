from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import login_required, current_user, UserMixin
from . import db
from .models import Note, Project
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user = current_user)

@views.route('/school')
def school():
    return render_template("school/school_menu.html")

@views.route('/tools')
def tools():
    return render_template("tools.html")

@views.route('/playlist')
def playlist():
    file_add = "website/static/files/playlist_analytic_view_counter.txt"

    file = open(file_add, "r").read()
    num = int(file)

    f = open(file_add, "w")
    f.write(str(num + 1))
    f.close()

    file = open(file_add, "r").read()
    return redirect('https://open.spotify.com/user/nobbe06n8xt2uo22yvdggbfhh?si=CI6uLIvmTsq7ebWNHTX9Gw')

@views.route('/playlist_an')
@login_required
def playlist_counter():
    file_add = "website/static/files/playlist_analytic_view_counter.txt"

    file = open(file_add, "r").read()

    if current_user.id == 1:
        return "<h1>"+ file +"</h1>"
    else:
        return redirect('https://open.spotify.com/user/nobbe06n8xt2uo22yvdggbfhh?si=CI6uLIvmTsq7ebWNHTX9Gw')

@views.route('/analytics')
def analytics():
    return render_template('analytics.html')
    
# |-------------------------------------------blog----------------------------------------------|
@views.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Post is too short!', category='error')
        else:
            new_note = Note(data = note, userId = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Post!', category='success')
    notes = Note.query.order_by(-Note.id)
    return render_template("blog.html", notes = notes)


@views.route('/deletePost', methods=['GET', 'POST'])
@login_required
def deleteUser():
    id = current_user.id
    if id == 1:
        if request.method == 'POST':
            userid = request.form.get('inputId') 
            Note.query.filter_by(id=userid).delete()
            db.session.commit()
            flash("Account deleted")
    return render_template('deleteUser.html')
# |---------------------------------------------------------------------------------------------|

# |-----------------------------------------portfolio-----------------------------------------------|
@views.route('/beta')
@login_required
def beta():
    return render_template('betaPortfolio/portfolio.html')

@views.route('/home')
def portfolio():
    return render_template("portfolio/portIndex.html")

@views.route('/about')
def about():
    return render_template("portfolio/about.html")

@views.route('/contact')
def contact():
    return render_template("portfolio/contact.html")

@views.route('/games')
def games():
    return render_template("betaPortfolio/games.html")

@views.route('/projects')
def projects():
    return render_template("portfolio/projects.html")
# |---------------------------------------------------------------------------------------------|

# |-----------------------------------------book report-----------------------------------------|
@views.route('/book-report')
def bookReport():
    return render_template("school/book report/book_report.html")

@views.route('/book-report/Gallery')
def bookReportGallery():
    return render_template("school/book report/Gallery.html")
# |---------------------------------------------------------------------------------------------|

# |-----------------------------------------Projects Essentials----------------------------------------|
@views.route('/essentials', methods=['GET', 'POST'])
@login_required
def essentials():

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        subject = request.form.get('subject')
        notebook = request.form.get('notebook')
        todo = request.form.get('todo') 

        new_Project = Project(name = name, userId = current_user.id, description = description, subject = subject, notebook = notebook, todo = todo)
        
        db.session.add(new_Project)
        db.session.commit()

        redirect("/projects")
        
        flash("project created", category = 'success')

    return render_template('tools/essentials.html')

@views.route('/projects-index')
@login_required
def projectasdadsds():
    projects = Project.query.order_by(Project.id)
    return render_template('tools/projects.html', projects = projects)

@views.route('/deleteProject/<id>')
@login_required
def deleteProject(id):
    projectId = id 
    Project.query.filter_by(id = projectId).delete()
    db.session.commit()
    flash("Project deleted")
    return redirect("/projects-index")

@views.route('/notebook')
def notebook():
    return render_template('tools/notebook.html')

@views.route('/to-do')
@login_required
def toDo():
    return render_template("tools/to_do_list.html")
# |---------------------------------------------------------------------------------------------|

# |--------------------------------------others-------------------------------------------------|

# |---------------------------------------------------------------------------------------------|