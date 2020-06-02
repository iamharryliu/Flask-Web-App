# Flask-Web-App
Base application for developing web apps.

### Installing
Create config file.
```
sudo nano /etc/config.json
```
```
{
        "SECRET_KEY":"your secret key",
        "SQLALCHEMY_DATABASE_URI":"sqlite:///site.db",
        "EMAIL_USERNAME":"your email",
        "EMAIL_PASSWORD":"your email password",
        "EMAIL_DEFAULT_SENDER":"your email"
        "ADMINS":[admin usernames]
}
```
```
git clone https://github.com/iamharryliu/Flask-Web-App.git
cd Flask-Web-App
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup_db.py
python run.py
```
