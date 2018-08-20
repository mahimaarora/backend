from backend import app
from domain import project_services

@app.route("/")
def index():
    return "Hello World"


@app.route("/add-project", methods = ['GET'])
def add_project():
    project_services.create_project()
    return "Project created!!"


@app.route('/user/<user-handle>')
def get_user_data():
    """This page will be called Users’ profile page. A user’s
    info will be shown to users. Info includes the languages
    they’ve experience in, a bio, their github handles and
    other links."""


@app.route('/project/<project-id>')
def project():
    """The page is a project specific page. This page is
    shown to all the users that are on the platform. This
    page contains public information about the project. This
    will also contain a link for project dashboard which will
    be shown only to the users who are part/collaborators of
    the project."""


@app.route('/user/dashboard')
def user_dashboard():
    """This page will be the dashboard for the user. The
    user will see all the projects they’ve created, they’re
    a part of. They’ll see their total income and income from
    each project. The projects shown here must be linked with
    each project dashboard page. Also the place to see their
    current discussions with prospective coworkers."""


@app.route('/project/dashboard/<project-id>')
def project_dashboard():
    """This page will be the dashboard for the project. The
    user will be able to see other collaborators and other
    features. It also has the current revenue generated by the
    project. Current GitHub activity can also be monitored with
    consent from the user."""


@app.route('/ideas')
def ideas():
    """This page will display ideas that different users put.
    The idea could require other people, post vacancies.
    Each idea will have upvote option and discussion panel.
    I prefer not having a different page for discussion. Just
    the existing idea would expand to show comments. Only the
    user who created the idea would be allowed to update it."""


@app.route('/products')
def products():
    """This page will showcase all the products that wish to
    be featured on our website."""


@app.route('/projects')
def projects():
    """Shows all of the projects in a single unified view."""


@app.errorhandler(500)
def internal_server_error(e):
    return 'Internal Server Error', 500


@app.errorhandler(404)
def page_not_found(e):
    return 'Page not found!', 404
