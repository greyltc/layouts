# using mechanical env here
```
python -m venv --without-pip --system-site-packages --clear venv
source venv/bin/activate
pushd ../../mechanical
python tools/venv_dev_install.py
popd
```
