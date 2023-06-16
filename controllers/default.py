# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
from gluon.utils import web2py_uuid as uuid

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def register():
    form = auth.register()
    return dict(form=form)

#@auth.requires_membership('admin') 
#@auth.requires_login()
#@auth.requires_permission('liste','utilisateur',1)
def liste_films():
    if auth.user:
        query = db.film.id > 0 
        films = db(query).select()
        return response.render('default/liste_films.html',dict(films=films))
    else:
        # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
        redirect(URL('default', 'user', args='login'))


# Contrôleur (controller)
def voir_affiche():
    entry_id = request.args(0)
    entry = db.affiche(entry_id)  # Remplacez "my_table" par le nom de votre table

    # Vérifier si l'entrée existe
    if entry is None:
        return "Entrée non trouvée"

    # Convertir les détails de l'entrée en un format approprié pour le rendu
    details = {
        'id': entry.id,
        'numero_affiche': entry.numero_affiche,
        'date_projection': entry.date_projection,
        'image': entry.image,
        # Ajoutez d'autres champs selon vos besoins
    }

    # Retourner les détails sous forme de réponse JSON
    return response.render('default/voir_affiche.html',dict(details=entry))



def liste_utilisateurs():
    query = db.utilisateur.id > 0 
    utilisateurs = db(query).select()
    return response.render('default/liste_utilisateurs.html',dict(utilisateurs=utilisateurs))


def liste_affiches():
    query = db.affiche.id > 0 
    affiches = db(query).select()
    return response.render('default/carousel.html',dict(affiches=affiches))


def liste_reservations():
    query = db.reservation.id > 0 
    reservations = db(query).select()
    return response.render('default/liste_reservations.html',dict(reservations=reservations))

def ajouter_film():
    form = SQLFORM(db.film)
    if form.process().accepted:
        redirect(URL('liste_films'))
    return dict(form=form)

def ajouter_utilisateur():
    form = SQLFORM(db.utilisateur)
    if form.process().accepted:
        redirect(URL('liste_utilisateurs'))
    return dict(form=form)

def ajouter_affiche():
    form = SQLFORM(db.affiche)
    if form.process().accepted:
        redirect(URL('liste_affiches'))
    return dict(form=form)

def ajouter_reservation():
    form = SQLFORM(db.reservation)
    if form.process().accepted:
        redirect(URL('liste_reservations'))
    return dict(form=form)


def modifier_film():  
    film = db.film(request.args(0)) or redirect(URL('liste_films'))
    form = SQLFORM(db.film, film)
    if form.process().accepted:
        redirect(URL('liste_films'))
    return dict(form=form)

def modifier_utilisateur():  
    utilisateur = db.utilisateur(request.args(0)) or redirect(URL('liste_utilisateurs'))
    form = SQLFORM(db.utilisateur, utilisateur)
    if form.process().accepted:
        redirect(URL('liste_utilisateurs'))
    return dict(form=form)

def modifier_affiche():  
    affiche = db.affiche(request.args(0)) or redirect(URL('liste_affiches'))
    form = SQLFORM(db.affiche, affiche)
    if form.process().accepted:
        redirect(URL('liste_affiches'))
    return dict(form=form)

def modifier_reservation():  
    reservation = db.reservation(request.args(0)) or redirect(URL('liste_reservations'))
    form = SQLFORM(db.reservation, reservation)
    if form.process().accepted:
        redirect(URL('liste_reservations'))
    return dict(form=form)


def supprimer_film():
    # Supprimer une film de la base de données
    db(db.film.id == request.args(0)).delete()
    redirect(URL('liste_films'))
    
    
def supprimer_utilisateur():
    # Supprimer une film de la base de données
    db(db.utilisateur.id == request.args(0)).delete()
    redirect(URL('liste_utilisateurs'))


def supprimer_affiche():
    # Supprimer une film de la base de données
    db(db.affiche.id == request.args(0)).delete()
    redirect(URL('liste_affiches'))
    
    
def supprimer_reservation():
    # Supprimer une film de la base de données
    db(db.reservation.id == request.args(0)).delete()
    redirect(URL('liste_reservations'))
    