## app.py
import os
from eduka import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


######################################
##                                  ##
##    import the blueprints here!   ##
##                                  ##
######################################

from eduka.users.views import users_blueprint
from eduka.posts.views import posts_blueprint
from eduka.core.views import core_blueprint
from eduka.utils.app_filters import filter_blueprint


######################################
##                                  ##
##    Register blueprints here!     ##
##                                  ##
######################################

app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(core_blueprint)
app.register_blueprint(filter_blueprint)

if __name__ == '__main__':
    app.run()
