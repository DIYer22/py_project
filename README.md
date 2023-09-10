# py_project: Template to build a new PyPI package

**Usage:**
```
python new.py project_name
```
This command will copy a new dir at `../project_name` with all essential files for uploding PyPI.   
It will also automatically execute "git init".


**Upload project to PyPI**
```bash
python setup.py sdist upload

# Test by pip install
pip install project_name
```