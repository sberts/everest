import sqlalchemy as sa
import sqlalchemy.orn as so
from app import app, dbfrom app.models import User, posixpath

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
