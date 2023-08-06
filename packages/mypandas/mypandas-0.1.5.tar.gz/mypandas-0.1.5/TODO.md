# Version 0

- [ ] DELETE FROM has no effect unless persist=True, should it?
- [ ] Problem calling MyPandas(URI, persist=True) twice, probably logic error of creating/deleting database twice?
- [ ] Fix remaining two pytest tests from pandasql
- [ ] Add MySQL syntax specific pytest tests in `test_mypandas.py`
- [ ] Fix dependencies not installing based on `pyproject.toml` setting

# Version 1

- [ ] Use sqlglot to transpile every dialect into sqlite, then you just need to support sqlite internally and then you can support every dialect, and the code actually gets simpler... Or you could leave in the current mysql/postgres/sqlite connection details and add the transpile logic. IMO it's annoying to provide a mysql connection. You could just do `MyPandas('mysql')(QUERY, locals())` instead of `MyPandas("mysql://root:root@localhost/")(QUERY, locals())`.
- [ ] Name change? If I'm supporting every dialect naming it MyPandas is confusing. Can't use `pandasql` it's used on pypi, come up with better name.
- [ ] Does sqlglot support paramaterized query transpilation?
- [ ] How do you tell if a string is a sqlalchemy connection? Maybe look at the internal code in https://docs.sqlalchemy.org/en/14/core/engines.html, or do something cheeky. Does some builtin like urlparse work because it's a URI?
- [ ] Copy the CD stuff from ty-command.
