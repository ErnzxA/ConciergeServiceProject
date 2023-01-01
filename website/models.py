from . import db  # import from website folder
from flask_login import UserMixin

user_service = db.Table('user_service',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('service_id', db.Integer, db.ForeignKey('service.service_id'))
                        )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150))
    company_name = db.Column(db.String(300))
    company_post = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    address = db.Column(db.String(150))
    birthdate = db.Column(db.Date)
    nationality = db.Column(db.String(150))
    image = db.Column(db.String(500), default='anonim.jpeg')
    role = db.Column(db.String(500), default='user')

    services = db.relationship('Service', secondary=user_service)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(150))


class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.String(150))
    service_icon_src = db.Column(db.String(150))
    service_img_src = db.Column(db.String(150))
    bg_img = db.Column(db.String(250))
    categories = db.relationship('Service_category')


class Service_category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(150))
    partners = db.relationship('Partners')
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'))



class Partners(db.Model):
    partner_id = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String(150), nullable=False)
    partner_city = db.Column(db.String(150), nullable=False)
    partner_price = db.Column(db.String(150), default='')
    partner_description = db.Column(db.String(150), default='')
    partner_image =  db.Column(db.String(150), nullable=False)
    partner_brand_img = db.Column(db.String(150), nullable=False)

    service_category_id = db.Column(db.Integer, db.ForeignKey('service_category.category_id'))


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.partner_id'))
    full_name = db.Column(db.String(150), nullable=False)
    price =  db.Column(db.Integer,nullable=False)
    file_src = db.Column(db.String(300), default='')
    id_src = db.Column(db.String(300), default='')
    date = db.Column(db.Date)





