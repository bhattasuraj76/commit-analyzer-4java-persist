from flask import Blueprint
from app.controllers import MainController, RepositoryController

bp = Blueprint("web_blueprint", __name__)

main_controller = MainController()
repository_controller = RepositoryController()


@bp.route('/', methods=['GET'])
def index():
    return main_controller.index()


@bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    return repository_controller.analyze()


@bp.route('/refresh', methods=['GET'])
def refresh():
    return repository_controller.refresh()


@bp.route('/compare', methods=['GET'])
def compare():
    return repository_controller.compare()


@bp.route('/compare-analyze', methods=['GET', 'POST'])
def compare_analyze():
    return repository_controller.compare_analyze()

@bp.route('/export', methods=['GET', 'POST'])
def export():
    return repository_controller.export()

@bp.route('/plotly', methods=['GET'])
def plotly():
    return repository_controller.plotly()