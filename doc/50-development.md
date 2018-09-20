# Development

## Requirements

### macOS

```
brew install python3 pandoc
```

### Pretix setup

```
python3 -m venv env
source env/bin/activate
pip3 install -U pip setuptools
export CXX=clang++
export CC=clang
cd src/
pip3 install -r requirements.txt -r requirements/dev.txt
```

### Local server

```
cd $HOME/coding/testing/pretix/pretix/src

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python make_testdata.py
python manage.py runserver
```

http://127.0.0.1:8000/control admin@localhost - admin

## Plugin setup

```
cd $HOME/coding/netways/pretix/pretix
source env/bin/activate
cd $HOME/coding/netways/pretix/pretix-invoice-net
```

```
python3 setup.py develop
```

## Plugin Release

### Create release


```
VERSION=0.0.4
```

```
sed -i "s/version = '.*'/version = '$VERSION'/g" setup.py
sed -i "s/archive\/.*'/archive\/v$VERSION.tar.gz'/g" setup.py

git commit -av -m "Release v$VERSION"
```


```
git tag -s -m "Version $VERSION" v$VERSION
```

```
python3 setup.py sdist
```

### PyPi Upload

#### Test

```
python setup.py sdist upload -r testpypi
```

#### Release

```
python setup.py sdist upload -r pypi
```
