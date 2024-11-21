python3 -m pytest -c .pytest.ini \
    --cov-config=.coveragerc \
    --cov=. \
    --cov-report term-missing
