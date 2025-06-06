from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Note, Category
from app.notes import notes_bp
from app.notes.forms import NoteForm


@notes_bp.route('/notes')
@login_required
def notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form = NoteForm()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    return render_template('notes.html', title='Notatki', notes=notes, form=form, categories=categories)


@notes_bp.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category_id.data if form.category_id.data else None,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Notatka została utworzona!', 'success')
        return redirect(url_for('notes.notes'))
    
    return render_template('create_note.html', title='Nowa notatka', form=form)


@notes_bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('Nie masz uprawnień do edycji tej notatki.', 'danger')
        return redirect(url_for('notes.notes'))
    
    form = NoteForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.category_id = form.category_id.data if form.category_id.data else None
        db.session.commit()
        flash('Notatka została zaktualizowana!', 'success')
        return redirect(url_for('notes.notes'))
    
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
        form.category_id.data = note.category_id
    
    return render_template('edit_note.html', title='Edycja notatki', form=form, note=note)


@notes_bp.route('/notes/<int:id>/delete', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('Nie masz uprawnień do usunięcia tej notatki.', 'danger')
        return redirect(url_for('notes.notes'))
    
    db.session.delete(note)
    db.session.commit()
    flash('Notatka została usunięta!', 'success')
    return redirect(url_for('notes.notes'))
