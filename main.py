import os
import sys
import logging
from flask import Flask
from api.utils.database import db, ma
from flask_jwt_extended import JWTManager
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from api.utils.email import mail
import api.utils.responses as resp
from api.utils.responses import response_with
from flask import send_from_directory
from api.routes.customers import customer_routes
from api.routes.users import user_routes


def create_app(app_config):
    app = Flask(__name__)
    
    # print(os.environ.get('WORK_ENV'))
    
    # if os.environ.get('WORK_ENV') == 'PROD':
        
    #     app_config = ProductionConfig
    # elif os.environ.get('WORK_ENV') == 'TEST':
    #     app_config = TestingConfig
    # else:
    #     app_config = DevelopmentConfig
    
    app.config.from_object(app_config)
    
    
    #routes
    app.register_blueprint(customer_routes, url_prefix='/api/customers')
    app.register_blueprint(user_routes, url_prefix='/api/users')
    
    jwt = JWTManager(app)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    
    
    
    @app.route('/photo/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
    
    # # START GLOBAL HTTP CONFIGURATIONS
    @app.after_request
    def add_header(response):
        return response
    
    
    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)
    
    
    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)
    
    
    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)
    
    # logging.basicConfig(stream=sys.stdout,
    #                     format='%(\
    #                     asctime)s|%(levelname)\
    #                     s|%(filename)s:%(lineno)s|%(message)s',\
    #                     level=logging.DEBUG)
    
    return app

# END GLOBAL HTTP CONFIGURATIONS
app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
    