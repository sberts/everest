from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    projects: so.WriteOnlyMapped['Project'] = so.relationship(
        back_populates='owner')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    project_name: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='projects')

    def __repr__(self):
        return '<Project {}>'.format(self.body)