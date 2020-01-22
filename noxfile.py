import shutil

import nox

py36 = '3.6'
py37 = '3.7'
py38 = '3.8'

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
	'lint',
	'doc',
	'test'
]


@nox.session
def lint(session):
	session.install('-U', '.[lint]')
	session.run('flake8', 'src/', 'tests/')


@nox.session
def doc(session):
	shutil.rmtree('docs/_build', ignore_errors=True)
	session.install('-U', '.[doc]')
	session.cd('docs')
	session.run(
		'sphinx-build',
		'-b',
		'html',
		'-W',
		'-d',
		'_build/doctrees',
		'.',
		'_build/html'
	)


@nox.session(python=[py36, py37, py38])
def test(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'pytest', *session.posargs)
	session.notify('report')


@nox.session(python=[py36, py37, py38])
def integration(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'pytest', '-m', 'integration', *session.posargs)
	session.notify('report')


@nox.session(python=[py36, py37, py38])
def unit(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'pytest', '-m', 'not integration', *session.posargs)
	session.notify('report')


@nox.session
def report(session):
	session.install('-U', 'coverage[toml]')
	session.run('coverage', 'report', '-m')
	session.run('coverage', 'erase')
