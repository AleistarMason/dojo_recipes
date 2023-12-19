from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe
from flask_app import app

@app.route('/recipes')
def recipes():
    if session.get('user_id'):
        recipes = recipe.Recipe.get_with_user()
        print(recipes)
        this_user = user.User.get_by_id(session['user_id'])
        return render_template('recipes.html', recipes = recipes, user = this_user)
    flash('Please login too access recipes!', 'login')
    return redirect('/')

@app.route('/recipes/new/')
def new_recipe():
    if session.get('user_id'):
        recipe_data = {
            'id': 0,
            'name': '',
            'description': '',
            'instructions': '',
            'date_cooked': None,
            'under_30': None
        }
        if session.get('return'):
            print(session['return'])
            recipe_data = session['return']
            print(recipe_data['date_cooked'])
            session.pop('return')
        return render_template('new_recipe.html', recipe = recipe_data)
    flash('Please login too access recipes!', 'login')
    return redirect('/')

@app.route('/recipes/edit/<int:id>/')
def edit_recipe(id):
    if session.get('user_id'):
        this_recipe = recipe.Recipe.get_by_id(id)
        return render_template('edit_recipe.html', recipe = this_recipe)
    flash('Please login too access recipes!', 'login')
    return redirect('/')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if session.get('user_id'):
        this_recipe = recipe.Recipe.get_by_id(id)
        this_user = user.User.get_by_id(session['user_id'])
        return render_template('view_recipe.html', recipe = this_recipe, user = this_user)
    flash('Please login too access recipes!', 'login')
    return redirect('/')

@app.route('/recipes/delete/<int:id>/')
def delete_recipe(id):
    if session.get('user_id'):
        if session['user_id'] == recipe.Recipe.get_by_id(id).creator.id:
            recipe.Recipe.delete(id)
        else:
            flash('This recipe can only be deleted by its creator!')
        return redirect('/recipes')
    flash('Please login too access recipes!', 'login')
    return redirect('/')

@app.route('/recipes/process', methods=['POST'])
def process():
    if request.form.get('process') == 'new':
        if recipe.Recipe.validate_new_recipe(request.form):
            recipe.Recipe.save(request.form)
        else:
            session['return'] = request.form
            return redirect('/recipes/new/')
    if request.form.get('process') == 'update':
        if recipe.Recipe.validate_new_recipe(request.form):
            recipe.Recipe.update(request.form)
        else:
            return redirect(f'/recipes/edit/{request.form["id"]}')
    return redirect('/recipes')