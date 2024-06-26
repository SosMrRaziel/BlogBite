from app import app, BlogBite

from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    """ Shell Context """
    return {'db': BlogBite, 'User': User, 'Post': Post}

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)