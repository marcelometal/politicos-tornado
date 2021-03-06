list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
no_targets__:

setup:
	@pip install -U -e .\[tests\]

test: drop_test data_test unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/unit/
	@coverage report -m --fail-under=80

focus:
	@coverage run --branch `which nosetests` -vv --with-yanc --with-focus -s tests/unit/

coverage-html: unit
	@coverage html

tox:
	@tox

drop:
	@-cd politicos/ && alembic downgrade base
	@$(MAKE) drop_now

drop_now:
	@mysql -u root -e "DROP DATABASE IF EXISTS politicos; \
		CREATE DATABASE IF NOT EXISTS politicos \
		DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
	@echo "DB RECREATED"

drop_test:
	@-cd tests/ && alembic downgrade base
	@mysql -u root -e "DROP DATABASE IF EXISTS test_politicos; \
		CREATE DATABASE IF NOT EXISTS test_politicos \
		DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
	@echo "DB RECREATED"

data:
	@cd politicos/ && alembic upgrade head

db: drop data

data_test:
	@cd tests/ && alembic upgrade head

sqltap:
	@open 'http://localhost:8000/report.html'; python -m SimpleHTTPServer

kill_run:
	@ps aux | awk '(/.+politicos-api.+/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

run:
	@politicos-api -vvv --debug -c ./politicos/config/__init__.py

publish:
	@python setup.py sdist upload

clean_pycs:
	@find . -name "*.pyc" -delete

.PHONY: clean_pycs coverage-html data data_test db drop drop_now drop_test focus kill_run list publish run setup sqltap test tox unit
