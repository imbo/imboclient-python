install:
	python setup.py install

clean:
	python setup.py clean --all

test:
	nosetests --nocapture -w imboclient/test/unit

integration-test:
	nosetests --nocapture -w imboclient/test/integration

