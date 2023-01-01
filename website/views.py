from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Service, user_service, Post, Partners, Order
from . import db, app  # import from website folder
from .data_floorproof import phone_num_floorproof
import os
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@views.route('/')
def home():
    return render_template("main.html", main_page="active", user=current_user)


@views.route('/contacts')
def contacts():
    return render_template("contacts.html", contacts="active", user=current_user)


# @views.route('/services')
# def all_services():
#     services = Service.query.all()
#     return render_template("services.html", our_services="active", services=services, user=current_user)


@login_required
@views.route('/services/create_new_service')
def create_new_service():
    if current_user.role != 'user':
        return render_template("create_service.html", our_services="active", user=current_user)
    else:
        return redirect(url_for('views.profile'))


@views.route('/services/<service_id>')
def service(service_id):
    try:
        service = Service.query.filter_by(service_id=service_id).first()
        return render_template("service.html", our_services="active", service=service, user=current_user)
    except:
        return redirect(url_for('views.all_services'))


@views.route('/services/<service_id>/<partner_id>', methods=['GET', 'POST'])
def order(service_id, partner_id):
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        count = request.form.get('count', type=int)
        userdate = request.form.get('userdate')
        info = request.form.get('info')
        partner = Partners.query.filter_by(partner_id=partner_id).first()
        price = int(''.join(partner.partner_price.split()))

        identity_card = request.files.get('identity_card')
        user_file = request.files.get('user_file')

        if identity_card.filename != '':
            newpath = fr'W:\Concierge Service\flaskProject\website\static\files\clients\{current_user.email}'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            app.config['UPLOAD_FOLDER'] = f'static/files/clients/{current_user.email}'
            identity_card.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                            secure_filename(identity_card.filename)))

        if user_file.filename != '':
            newpath = fr'W:\Concierge Service\flaskProject\website\static\files\clients\{current_user.email}'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            app.config['UPLOAD_FOLDER'] = f'static/files/clients/{current_user.email}'
            user_file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                        secure_filename(user_file.filename)))

        user_date = userdate.split('-')
        from datetime import date
        user_date = date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

        new_order = Order(user_id=current_user.id,
                        partner_id=partner_id,
                        full_name=full_name,
                        price = price*count,
                        file_src=user_file.filename,
                        id_src=identity_card.filename,
                        date=user_date)

        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('views.profile'))

    # app.config['UPLOAD_FOLDER'] = f'static/files/clients/{current_user.email}'
    from datetime import date

    current_date = date.today()
    return render_template("order.html", our_services="active", current_date=current_date, user=current_user)


@views.route('/profile')
@login_required
def profile():
    if current_user.role == 'user':
        return render_template("user_profile.html", profile="active", user=current_user)
    else:
        return render_template("admin_profile.html", profile="active", user=current_user)


@views.route('/profile/change', methods=['GET', 'POST'])
@login_required
def change_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        company_name = request.form.get('company_name')
        company_post = request.form.get('company_post')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        birthdate = request.form.get('birthdate')
        nationality = request.form.get('nationality')

        image = request.files.get('image')

        update_user = User.query.filter_by(email=current_user.email).first()

        if full_name != 'None':
            update_user.full_name = full_name

        if company_name != 'None':
            update_user.company_name = company_name

        if company_post != 'None':
            update_user.company_post = company_post

        if address != 'None':
            update_user.address = address

        if phone_number != 'None':
            if phone_num_floorproof(phone_number):
                update_user.phone_number = phone_number
            else:
                flash('Некоректный номер')
                return redirect(url_for('views.change_profile'))

        if nationality != 'None':
            update_user.nationality = nationality

        if birthdate != '':
            birthdate = birthdate.split('-')
            from datetime import date
            update_user.birthdate = date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))

        services_id = set([int(i) for i in request.form.getlist('checkbox_service')])
        user_services_id = set([i.service_id for i in update_user.services])

        for i in list(services_id - user_services_id):
            service = Service.query.filter_by(service_id=i).first()
            update_user.services.append(service)

        for i in list(user_services_id - services_id):
            service = Service.query.filter_by(service_id=i).first()
            update_user.services.remove(service)

        if image.filename != '':
            app.config['UPLOAD_FOLDER'] = 'static/files/user_image'
            if update_user.image == 'anonim.jpeg' or update_user.image == '':
                image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                        secure_filename(image.filename)))
                update_user.image = secure_filename(image.filename)
            else:
                try:
                    os.unlink(os.path.join(app.root_path, 'static/files/user_image/' + update_user.image))
                except:
                    print('Photo does not exist')
                image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                        secure_filename(image.filename)))
                update_user.image = secure_filename(image.filename)

        db.session.commit()

        return redirect(url_for('views.profile'))
    from datetime import date
    current_date = date.today()
    services = Service.query.all()
    return render_template("change_profile.html", profile="active", user=current_user, services=services,
                           current_date=current_date)


@views.route('/profile/clients/page-<page>', methods=['GET', 'POST'])
@login_required
def service_clients(page):
    if current_user.role != 'user':
        option_selected = 'all'
        users = []
        user_count = 1
        if request.method == 'POST':
            option_selected = request.form.get('options')
            serach_data = request.form.get('serach')
            if option_selected == 'all':
                users = User.query.filter(User.email.ilike("%" + serach_data + "%"),
                                          User.email.ilike("%" + serach_data.capitalize() + "%")).all()
                user_count = User.query.filter(User.email.ilike("%" + serach_data + "%"),
                                               User.email.ilike("%" + serach_data.capitalize() + "%")).count()
            else:
                users = User.query.filter_by(role=option_selected).filter(User.email.ilike("%" + serach_data + "%"),
                                                                          User.email.ilike(
                                                                              "%" + serach_data.capitalize() + "%")).all()
                user_count = User.query.filter_by(role=option_selected).filter(
                    User.email.ilike("%" + serach_data + "%"),
                    User.email.ilike("%" + serach_data.capitalize() + "%")).count()

        if not users and user_count > 0:
            users = User.query.all()
            user_count = User.query.count()
        roles = Post.query.all()
        disable_start = ''
        disable_end = ''
        endpage = int(page) * 5
        if int(page) * 5 > user_count:
            endpage = user_count
            disable_end = 'disabled'

        if page == '1':
            disable_start = 'disabled'
        return render_template("user_list.html", profile="active", option_selected=option_selected,
                               user_count=user_count, page=int(page) * 5,
                               endpage=endpage, users=users, roles=roles, disable_start=disable_start,
                               disable_end=disable_end,
                               user=current_user)
    else:
        return redirect(url_for('views.profile'))


@views.route("/profile/delete/user/<email>", methods=['GET', 'POST'])
@login_required
def delete_user(email):
    if current_user.role != 'user':
        try:
            user = User.query.filter_by(email=email).first()
            if current_user.role == 'director' and user.role != 'director' or current_user.role == 'moderator' and \
                    user.role == 'user':
                db.session.delete(user)
                db.session.commit()
        except:
            return redirect(url_for('views.service_clients', page='1'))

    return redirect(url_for('views.service_clients', page='1'))


@views.route("/profile/promote/user/<email>", methods=['GET', 'POST'])
@login_required
def promote_user(email):
    if current_user.role != 'user':
        try:
            user = User.query.filter_by(email=email).first()
            if current_user.role == 'director' and user.role == 'user':
                user.role = 'moderator'
                user.company_name = 'Concierge Service'
                db.session.commit()
        except:
            return redirect(url_for('views.service_clients', page='1'))

    return redirect(url_for('views.service_clients', page='1'))


@views.route('/profile/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if current_user.role != 'user':
        return render_template('chat.html', profile="active", user=current_user)
    else:
        return redirect(url_for('views.profile'))