from . import db
from .auth import current_user, Blueprint, redirect, render_template, request, flash
from .models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
def home():
    if current_user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title != "" and desc != "":
            note = Note(Title=title, Description=desc, user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash("<strong>Success:</strong> You Todo has Been Added!", "success")
    note = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", allTodo=note, enumerate=enumerate)


@views.route("/delete/<int:id>")
def Delete(id):
    todo = Note.query.filter_by(id=id, user_id=current_user.id).all()
    if len(todo) == 0:
        flash("<strong>Error:</strong> That Todo doesn't Belongs To You OR It doesn't Exists!", category="danger")
        return redirect("/")
    todo = todo[0]
    db.session.delete(todo)
    db.session.commit()
    flash("<strong>Success:</strong> That Todo has Been deleted", "success")
    return redirect("/")
