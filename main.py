from flask import Flask
from api.utils.database import db, ma
from flask_jwt_extended import JWTManager
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from api.utils.email import mail
from flask import send_from_directory
from api.routes.customers import customer_routes
from api.routes.users import user_routes


def create_app(app_config):
    app = Flask(__name__)
    

    app.config.from_object(app_config)
    
    
    #routes
    app.register_blueprint(customer_routes, url_prefix='/api/customers')
    app.register_blueprint(user_routes, url_prefix='/api/users')
    
    #route for upload photo
    @app.route('/photo/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
    jwt = JWTManager(app)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    
        
    return app



app = create_app(DevelopmentConfig)
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
    