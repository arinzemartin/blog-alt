from flask import Flask, render_template
from .config.variables import SECRET_KEY
import os

# GETS THE FOLDER (ABSOLUTE) NAME FOR THE `__init__.py` -> something.../blog/
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
  app = Flask(__name__) 

  # CONFIGS
  app.config["SECRET_KEY"] = SECRET_KEY
  # JOINS THE BASE DIRECTORY WITH /static/uploads -> something.../blog/static/uploads/
  app.config["BLOG_UPLOAD_PATH"] = os.path.join(BASE_DIR, "static/uploads/") 
  app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 # 2MB


  # BLUEPRINT
  from .views.admin_auth import admin
  app.register_blueprint(admin, url_prefix="/owner")

  from .views.category import category
  app.register_blueprint(category, url_prefix="/owner/category")

  from .views.article import article
  app.register_blueprint(article, url_prefix="/owner/article")


  # ERROR 404
  @app.errorhandler(404)
  def page_not_found(error):
    print("404 ERROR:", str(error))
    return render_template("error-404.html")
  

  # ERROR 500
  # @app.errorhandler(Exception)
  # def server_error(error):
  #   print("500 ERROR:", str(error))
  #   return render_template("error-500.html")
  

  return app