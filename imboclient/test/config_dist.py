# In order to run integration tests against a true IMBO instance copy this file to "config.py" and run "make integration-test".
# WARNING: as these tests modify the actual data a separate public key for the testing environment is HIGHLY recommended and REQUIRED to avoid unexpected loss of data
server = {
        "host": "REPLACE",
        "public": "REPLACE",
        "private": "REPLACE"
        }

