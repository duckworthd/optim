PROJECT = optim
ENV     = env

dependencies:
	test -e $(ENV) || virtualenv $(ENV) --system-site-packages
	. $(ENV)/bin/activate; pip install pip setuptools --upgrade
	. $(ENV)/bin/activate; pip install -r requirements.txt --use-wheel

develop: dependencies
	. $(ENV)/bin/activate; python setup.py develop

install: dependencies
	. $(ENV)/bin/activate; python setup.py install

clean:
	find $(PROJECT) -iname "*.pyc" | xargs -I {} rm "{}"
	rm -rf *.egg-info

cleanenv: clean
	rm -rf $(ENV)

publish: test
	echo "Are you sure you really want to publish to PyPI? [yN] "; \
	read really_push;                                              \
	if [[ "$$really_push" == "y" ]]; then                          \
		. $(ENV)/bin/activate; python setup.py sdist upload;         \
		echo "Publishing.";                                          \
	else                                                           \
		echo "Not publishing."; 																	   \
	fi

test: dependencies
	. $(ENV)/bin/activate; python -m nose
