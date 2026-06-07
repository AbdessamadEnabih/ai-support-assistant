from database import Base
from sqlalchemy.orm import Mapped, mapped_column, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import String, event
from typing import Optional
import bcrypt


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    firstname: Mapped[str] = mapped_column(String(30), nullable=False)
    lastname: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname = column_property(firstname + " " + lastname)
    # Email field: Indexed for fast login lookups, unique, and strictly limited in length
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )

    # Password infrastructure
    _password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    @hybrid_property
    def password(self):
        return AttributeError("Password is not readable attribure.")

    @password.setter
    def password(self, plaintext_password: str):
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)
        self.password_hash = hashed_bytes.decode("utf-8")

    def check_password(self, plaintext_password: str) -> bool:
        return bcrypt.checkpw(plaintext_password.encode("utf-8"), self._password_hash)
    
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.fullname!r}, email={self.email!r})"
