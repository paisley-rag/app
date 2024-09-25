# Testing
- note:  app repo should be cloned into a folder `db`
- run tests from the parent directory of where the app is located
  - `python -m pytest db` : runs pytest for the module "db"
  - this is required since all imports within Paisley reference a folder `db`
