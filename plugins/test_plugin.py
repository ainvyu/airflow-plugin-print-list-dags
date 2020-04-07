from subprocess import Popen, PIPE

# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_admin import BaseView, expose
from flask_admin.base import MenuLink

#from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask_appbuilder import BaseView as AppBuilderBaseView

# Creating a flask admin BaseView
class TestView(BaseView):
    def get_output_execute_list_dags(self):
        process = Popen(["airflow", "list_dags"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        return output

    @expose('/')
    def test(self):
        return self.get_output_execute_list_dags()

v = TestView(category="Test Plugin", name="Test View")

ml = MenuLink(
    category='Test Plugin',
    name='Test Menu Link',
    url='https://airflow.apache.org/')

# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "test_plugin", __name__,
    template_folder='templates', # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/static/test_plugin')


"""
################################################################################
class DebugDagsAppBuilder(AppBuilderBaseView):
    default_view = "render_result_list_dags"

    def get_output_execute_list_dags(self):
        process = Popen(["airflow", "list_dags"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        return output

    @expose("/")
    def render_result_list_dags(self):
        return self.get_output_execute_list_dags()

v_appbuilder_view = DebugDagsAppBuilder()
v_appbuilder_package = {"name": "Test View",
                        "category": "Test Plugin",
                        "view": v_appbuilder_view}

# Creating a flask appbuilder Menu Item
appbuilder_mitem = {"name": "Google",
                    "category": "Search",
                    "category_icon": "fa-th",
                    "href": "https://www.google.com"}
"""


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"

    admin_views = [v]
    flask_blueprints = [bp]
    menu_links = [ml]
    #appbuilder_views = [v_appbuilder_package]
    #appbuilder_menu_items = [appbuilder_mitem]
