from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.models import Category
from app.categories import categories_bp
from app.categories.forms import CategoryForm


@categories_bp.route('/')
@login_required
def index():
    """Display the list of user's categories."""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories/index.html', title='Categories', categories=categories)


@categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new category."""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('categories.index'))
    return render_template('categories/create.html', title='New category', form=form)


@categories_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing category."""
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('You do not have permission to edit this category.', 'danger')
        return redirect(url_for('categories.index'))
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.color = form.color.data
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('categories.index'))
    return render_template('categories/edit.html', title='Edit category', form=form, category=category)


@categories_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """
    Usuwa kategorię.
    
    Args:
        id: ID kategorii do usunięcia.
    
    Returns:
        jsonify: Odpowiedź JSON z informacją o sukcesie lub błędzie.
    """
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        return jsonify({'error': 'Nie masz uprawnień do usunięcia tej kategorii.'}), 403
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return jsonify({'success': True})


@categories_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form = CategoryForm()
    return render_template('categories.html', title='Kategorie', categories=categories, form=form)


@categories_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('categories.categories'))
    return render_template('create_category.html', title='Nowa kategoria', form=form)


@categories_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('Nie masz uprawnień do edycji tej kategorii.', 'danger')
        return redirect(url_for('categories.categories'))
    
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('categories.categories'))
    
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    
    return render_template('edit_category.html', title='Edycja kategorii', form=form, category=category)


@categories_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('Nie masz uprawnień do usunięcia tej kategorii.', 'danger')
        return redirect(url_for('categories.categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('categories.categories'))
