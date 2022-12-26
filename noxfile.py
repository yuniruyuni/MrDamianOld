import nox_poetry


@nox_poetry.session
def lint(session):
    session.run('pflake8')
