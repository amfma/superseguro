from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class Base(DeclarativeBase):
    pass

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(64), index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contenido(db.Model):
    __tablename__ = 'contenido'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    texto: Mapped[str] = mapped_column(db.Text, nullable=False)
    boolean : Mapped[bool] = mapped_column(db.Boolean, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))