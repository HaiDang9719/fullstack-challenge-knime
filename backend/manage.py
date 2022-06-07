import unittest
from flask_script import Manager
from app import blueprint
from flask_cors import CORS
from app.main.utils.starting_actions import create_data_index
from app.main import create_app
app = create_app('dev')
app.register_blueprint(blueprint)
app.app_context().push()

CORS(app)

# Flask script manager for custom scripts
manager = Manager(app)


@manager.command
def run():
    print("App is starting...")
    create_data_index()
    app.run(port=7200, host='0.0.0.0', debug=True)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
