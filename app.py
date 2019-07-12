## app.py
# -*- coding: utf-8 -*-
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


## utils
from eduka.utils.app_filters import filter_blueprint

## error pages blueprints
from eduka.error_pages.handlers import error_pages_blueprint



######################################
##                                  ##
##    Register blueprints here!     ##
##                                  ##
######################################

app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(core_blueprint)
app.register_blueprint(filter_blueprint)
app.register_blueprint(error_pages_blueprint)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
    # to run app so on ip 192.168.1.29:5000
    ## using the computer ip address instead of
    ## 127.0.0.1:5000 the localhost
