## Flask-SQLAlchemy

* Flask-SQLAlchemy is an extension for [Flask](https://flask.palletsprojects.com/en/1.1.x/) that adds support for [SQLAlchemy](https://www.sqlalchemy.org/) to your application. 
* It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.
* Flask-SQLAlchemy is fun to use, incredibly easy for basic applications, and readily extends for larger applications.

## SQLAlchemy

* SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

**Note:** For the complete guide, checkout the API documentation on the [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) class.

### Requirements

| Our Version             | Python                  | Flask                   | SQLAlchemy              |
|-------------------------|-------------------------|-------------------------|-------------------------|
| 2.x                     | 2.7, 3.4+               | 0.12+                   | 0.8+ or 1.0.10+ w/      |
|                         |                         |                         | Python 3.7              |
| 3.0+ (in dev)           | 2.7, 3.5+               | 1.0+                    | 1.0+                    |

### Prerequisites

* Install Python using PPA (Personal Package Archive)

  * Install the following requirements:
    ```
    sudo apt-get install software-properties-common python-software-properties
    ```
  * Run the following command to add the PPA
    ```
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```
  * Update
    ```
    sudo add-get update
    ```
  * Install Python 3.6
    ```
    sudo apt-get install python3.6
    ```
  * You can check the installed version by using this command
    ```
    python3.6 --version
    ```

* Check if pip (The python package installer) is already installed by running
  ```
  pip --version
  ```
  * If installed then upgrade it using the command
    ```
    python -m pip install --upgrade pip
    ```
    **Note:** This will upgrade the pip version


* Install virtual environment
  ```
  pip install virtualenv
  ```
  * Create python3.6 virtual environment
    ```
    virtualenv -p python3.6 venv
    ```
  * Activate virtual environment
    ```
    source venv/bin/activate
    ```
    
* Install Flask (version 1.0.2)
  ```
  pip install Flask==1.0.2
  ```

* Install Flask-SQLAlchemy (version 2.3.2)
  ```
  pip install Flask-SQLAlchemy==2.3.2
  ```
  **Note:** You can use any version of **Python**, **Flask** & **Flask-SQLAlchemy** depending on the **Requirements** as stated above

### Create an Application

* To create your Flask application, load the [configuration](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) of choice and then create the [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) object by passing it the application.
Once created, that object then contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm. Furthermore it provides a class called Model that is a declarative base which can be used to declare models:

```
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = SQLAlchemy(app)


    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username
```
**Note:** Save this as __repr__.py file

* To run this file using the terminal, use the command

  ```
  env FLASK_APP=__repr__.py flask run
  ```

* Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
  **Note:** Press CTRL+C to quit using the terminal

* To create the initial database, just import the db object from an **interactive Python shell** and run the **SQLAlchemy.create_all()** method to create the tables and database:
  ```
  >>> from yourapplication import db
  >>> db.create_all()
  ```
  Done, that's your database

* Now to create some users continuing with the **interactive python shell**:
  ```
  >>> from yourapplication import User
  >>> admin = User(username='admin', email='admin@example.com')
  >>> guest = User(username='guest', email='guest@example.com')
  ```

* The admin & the guest are not in the database yet, to make sure they are add them to the database
  ```
  >>> db.session.add(admin)
  >>> db.session.add(guest)
  >>> db.session.commit()
  ```

* To access the data in the database
  ```
  >>> User.query.all()
      [<User u'admin'>, <User u'guest'>]
  >>> User.query.filter_by(username='admin').first()
      <User u'admin'>
  ```
* When you are done using the app, deactivate the virtual environment by using the command
  ```
  deactivate
  ```

## API

### Usage Modes

Depending on how you initialize the object it is usable right away or will attach as needed to a Flask application.
There are two usage modes which work very similarly.

* First usage mode
  One is binding the instance to a very specific Flask application:
  ```
  app = Flask(__name__)
  db = SQLAlchemy(app)
  ```

* Second usage mode
  The second possibility is to create the object once and configure the application later to support it:
  ```
  db = SQLAlchemy()

  def create_app():
      app = Flask(__name__)
      db.init_app(app)
      return app
  ```

The difference between the two is that in the first case methods like create_all() and drop_all() will work all the time but in the second case a flask.Flask.app_context() has to exist.

**Note:**
* An init_app() method is a way of constructing an instance of the particular package, then letting it know about the Flask instance (so that configuration details can be copied). Mechanically, it's just like any other instance method.
* create_all() Creates all tables.
* drop_all() Drops all tables.
* app_context() 
Create an [AppContext](https://flask.palletsprojects.com/en/1.1.x/api/#flask.ctx.AppContext). Use as a with block to push the context, which will make current_app point at this application.

## Usage of Flask-SQLAlchemy in mentorship-backend

In the mentorship-backend the app is created using the second possibility as mentioned in **API Usage Modes** above:

* The SQLAlchemy object is created first, you can view the file [here](https://github.com/anitab-org/mentorship-backend/blob/develop/app/database/sqlalchemy_extension.py)
  ```
  from flask_sqlalchemy import SQLAlchemy

  db = SQLAlchemy()
  ```
  **Note:** db is the SQLAlchemy object

* Then the [flask app](https://github.com/anitab-org/mentorship-backend/blob/develop/run.py) is created which can be configured later to support the SQLALchemy object
											
  * Function for the creation of the Flask Application is
    ```
    def create_app(config_filename: str) -> Flask:
    ```
  * Creation of Flask Application & loading the configuration of choice
    ```
    app = Flask(__name__)
    # setup application environment
    app.config.from_object(config_filename)
    ```
  * The SQLAlchemy object **db** that has been created in sqlalchemy_extension.py module has been imported to the run.py module using:
    ```
    from app.database.sqlalchemy_extension import db
    ```
  * An init_app() method is used which is a way of constructing an instance of the particular package, then letting it know about the Flask instance (so that configuration details can be copied). Mechanically, it's just like any other instance method.
    ```
    db.init_app(app)
    ```
  * The Flask App can be loaded with the configuration of choice 
    ```
    application = create_app(get_env_config())
    ```

  **Note:** 
  * Here the create_app() calls the get_env_config() which can be found 
    [here](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L138) which contains the FLASK_ENVIORNMENT_CONFIG as "prod", "test", "dev", "local", "stag"
    ```
    def get_env_config() -> str:
        flask_config_name = os.getenv("FLASK_ENVIRONMENT_CONFIG", "dev")
        if flask_config_name not in ["prod", "test", "dev", "local", "stag"]:
           raise ValueError(
               "The environment config value has to be within these values: prod, dev, test, local, stag."
      )
        return CONFIGURATION_MAPPER[flask_config_name] 
    ```

   * The get_env_config() returns the [CONFIGURATION_MAPPER](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L147) as shown
     ```
     CONFIGURATION_MAPPER = {
         "dev": "config.DevelopmentConfig",
         "prod": "config.ProductionConfig",
         "stag": "config.StagingConfig",
         "local": "config.LocalConfig",
         "test": "config.TestingConfig",
     }
     ```

### Configuration

The following configuration values exist for Flask-SQLAlchemy. Flask-SQLAlchemy loads these values from your main Flask config which can be populated in various ways. Note that some of those cannot be modified after the engine was created so make sure to configure as early as possible and to not modify them at runtime.

A list of configuration keys currently understood by the extension can be found [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)

* The FLASK_ENV_CONFIG used in the the mentorship-backend are:
  * prod
  * test
  * dev
  * local
  * stag

* Among the various [configuration keys](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) understood by the extension we take SQLALCHEMY_DATABASE_URI into consideration.

**Note:** SQLALCHEMY_DATABASE_URI: The database URI that should be used for the connection. 
URI or Uniform Resource Identifier is a string of characters that unambiguously identifies a particular resource.

 * The SQLALCHEMY_DATABASE_URI for various FLASK_ENV_CONFIG are:

   * [prod](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L98)
     ```
     class ProductionConfig(BaseConfig):
         """Production configuration."""

         SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
         MOCK_EMAIL = False
     ```

   * [dev](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L105)
     ```
     class DevelopmentConfig(BaseConfig):
         """Development configuration."""

         DEBUG = True
         SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
     ```

   * [stag](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L112)
     ```
     class StagingConfig(BaseConfig):
         """Staging configuration."""

         DEBUG = True
         SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
         MOCK_EMAIL = False
     ```

**Note:** For the above FLASK_ENV_CONFIG there is a function build_db_uri associated which can be found [here](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L80), this is to build remote database URI using specific enviornment variables

   * [local](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L119)
     ```
     class LocalConfig(BaseConfig):
         """Local configuration."""

         DEBUG = True

         # Using a local sqlite database
         SQLALCHEMY_DATABASE_URI = "sqlite:///local_data.db"
     ```

   * [test](https://github.com/anitab-org/mentorship-backend/blob/eae562267b1cbbb597ea3a8829b87ad373fa323c/config.py#L128)
     ```
     class TestingConfig(BaseConfig):
         """Testing configuration."""

         TESTING = True
         MOCK_EMAIL = True

         # Use in-memory SQLite database for testing
         SQLALCHEMY_DATABASE_URI = "sqlite://"
     ```

* To create all tables  
  ```
  def create_tables():
      from app.database.sqlalchemy_extension import db

      db.create_all()
  ```

* You can run the app by using the command
  ```
  python run.py
  ```

* Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser

  **Note:** Press CTRL+C to quit



