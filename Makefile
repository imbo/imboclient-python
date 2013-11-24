install:
	python setup.py install

clean:
	python setup.py clean --all

test:
	nosetests -w imboclient/test/unit

integration-test:
	nosetests -w imboclient/test/integration

