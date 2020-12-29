from flask import render_template


def index():
    site_config = {
        'title': 'stockbag'
    }
    return render_template('index.html', config=site_config)
