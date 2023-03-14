from flask import render_template, request, url_for, redirect


class MainController:
    def __init__(self):
        pass

    def index(self):
        url = request.args.get("url")
        if url:
            # Preserve the used HTTP method
            return redirect(url_for('web_blueprint.analyze_repository', code=307))
        else:
            return render_template('pages/index.html')
