.PHONY: clean

clean:
	@clear
	@date
	rm -rf school/fixtures/generated/*
	python3 manage.py migrate school zero
	python3 manage.py migrate school
	python3 seeds.py
	@date

test-enrollment:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments
	@date

test-enrollment-serializer:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentSerializerTestCase
	@date

test-enrollment-model:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentModelTestCase
	@date

test-enrollment-model-create:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentModelTestCase.test_create
	@date

test-user-auth:
	@clear
	@date
	python3 manage.py test school.tests.test_authentication.AuthenticationUserTestCase
	@date

test-curl:
	@clear
	@date
	./test_endpoint.sh gen_get LOCAL school/courses/ admin:A12345678a | jq
	@date

ctags:
	@clear
	ctags --options=.ctags -R .
	ctags --options=.ctags -R -e .

syslink:
	@clear
	ln -s .credentials/.env-mysql .env
	ln -s .credentials/.my_local.cnf .my.cnf

dump-fixture-model:
	@clear
	@date
	@echo "" > school/fixtures/model.json
	python3 manage.py dumpdata school.course | jq > school/fixtures/model.json
	@date

generate-secrets-flask:
	@python3 -c 'import secrets; print(secrets.token_hex())'
	@python3 -c "from flask_bcrypt import generate_password_hash; print(generate_password_hash('A12345678a').decode('utf-8'))"

run:
	@flask run --host=0.0.0.0 --port=5000
	# Alternative: using -m to make import ..helper viable
	@python3 -m app

terraform_db:
	@mysql --defaults-extra-file=.my.cnf < database/terraform.sql

db:
	@clear
	@date
	mysql --defaults-extra-file=.my.cnf < database/ddl.sql
	mysql --defaults-extra-file=.my.cnf < database/seed.sql
