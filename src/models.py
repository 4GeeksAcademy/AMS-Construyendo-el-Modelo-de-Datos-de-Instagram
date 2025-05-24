from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_registro: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    posts = relationship('Post', back_populates='usuario', cascade="all, delete-orphan")
    comentarios = relationship('Comentario', back_populates='usuario', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='usuario', cascade="all, delete-orphan")
    seguidores = relationship('Follower', foreign_keys='Follower.user_id', back_populates='usuario', cascade="all, delete-orphan")
    siguiendo = relationship('Follower', foreign_keys='Follower.follower_id', back_populates='seguidor', cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "nombre": self.nombre,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None
        }

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    usuario = relationship('User', back_populates='posts')
    comentarios = relationship('Comentario', back_populates='post', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='post', cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "imagen_url": self.imagen_url,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id: Mapped[int] = mapped_column(primary_key=True)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    usuario = relationship('User', back_populates='comentarios')
    post = relationship('Post', back_populates='comentarios')

    def serialize(self):
        return {
            "id": self.id,
            "contenido": self.contenido,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "usuario_id": self.usuario_id,
            "post_id": self.post_id
        }

class Like(db.Model):
    __tablename__ = 'like'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    usuario = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "post_id": self.post_id,
            "fecha": self.fecha.isoformat() if self.fecha else None
        }

class Follower(db.Model):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)      # El usuario que es seguido
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)   # El usuario que sigue
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    usuario = relationship('User', foreign_keys=[user_id], back_populates='seguidores')
    seguidor = relationship('User', foreign_keys=[follower_id], back_populates='siguiendo')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "follower_id": self.follower_id,
            "fecha": self.fecha.isoformat() if self.fecha else None
        }
