# AMRTrack: Antimicrobial Suite
**Open-Source Antimicrobial Suite** coded in **Django Framework** on top of **Adminator Dashboard** design. 

**Features**:
- RDMS, Django native ORM
- Modular design
- Session-Based authentication (login, register)
- Forms validation
- Resposive UI Kit
<br />

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/raptor419/AMRTrack-AIIMS.git
$ cd django-dashboard-adminator
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv --no-site-packages env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv --no-site-packages env
$ # .\env\Scripts\activate
$ 
$ # Install modules
$ # SQLIte version
$ pip install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port 
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

<br />

## Support

- Available support via eMail harsh17234@iiitd.ac.in, samarth18410@iiitd.ac.in 

<br />

## Credits & Links
- [Tavlab](https://tavlab.iiitd.edu.in)
- [Django Framework](https://www.djangoproject.com/) - Offcial website

<br />

## License

@MIT

<br />
