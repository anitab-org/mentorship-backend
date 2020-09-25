## Flask-SQLAlchemy

Flask-SQLAlchemy is an extension for [Flask](https://flask.palletsprojects.com/en/1.1.x/) that adds support for [SQLAlchemy](https://www.sqlalchemy.org/) to your application.

## SQLAlchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
Or simply it can be understood as a database toolkit for python. It represents end-to-end system for working with python DBAPI (Database API), relational databases, & the SQL language.It provides helpers, tools & components to assist with database development at every level.

Two main components of SQLAlchemy:
* SQLAlchemy Core
* SQLAlchemy ORM

### SQLAlchemy Core

* **Engine** - a registry (object in a computer or an application that stores some common repository of information about something) which provides connectivity to a particular database server. In this case the engine stores information about the database it is connected to.
* **Dialect** - interprets generic SQL and database commands in terms of a specific DBAPI and database backend.
* **Connection Pool** - holds a collection of database connections in memory for fast re-use.
* **SQL Expression Language** - Allows SQL satements to be written using Python expressions.
* **Schema/Types** - Uses Python objects to represent tables, columns, and datatypes.

### SQLAlchemy ORM

SQLAlchemy is most famous for its object-relational mapper (ORM) or Object-relational mapping is a technique for storing, retrieving, updating, and deleting from an object-oriented program in a relational database.

* The ORM allows construction of python object which can be mapped to relational database tables
* Transparently persists objects(like the state of a python object) into their corresponding database tables using the unit of work pattern.
* Provides a query system which loads objects and attributes using SQL generated from mappings.
* Builds on top of the core- uses the Core to generate SQL and talk to the database.

**Note:** For the complete guide, checkout the API documentation on the [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) class.

### Requirements

| Our Version             | Python                  | Flask                   | SQLAlchemy              |
|-------------------------|-------------------------|-------------------------|-------------------------|
| 2.x                     | 2.7, 3.4+               | 0.12+                   | 0.8+ or 1.0.10+         |
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

To create your Flask application, load the [configuration](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) of choice and then create the [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) object by passing it the application.
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
            username = f'User: {self.username}'
            return username
```
**Note:** Save this as test.py file.Make sure to not call your application flask.py because this would conflict with Flask itself.

## So what did the above code do?

* First we imported the [Flask](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask) class & then the [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy) class.

* Next we create an instance of this class. The first argument is the name of the application module or package. If you are using a single module (as in this example), you should use \__name__ because depending on if it’s started as application or imported as module the name will be different ('\__main__' versus the actual import name). This is needed so that Flask knows where to look for templates, static files, and so on.

* Applications need some kind of configuration. There are different settings you might want to change depending on the application environment like toggling the debug mode, setting the secret key, and other such environment-specific things.
  **config** behaves exactly like a regular dictionary but supports additional methods to load a config from files.

* Connecting to a database: The **Engine** is the starting point for any SQLAlchemy application. It’s “home base” for the actual database and its DBAPI, delivered to the SQLAlchemy application through a connection pool and a Dialect. The general structure & more information can be found [here](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls). An Engine references both a Dialect and a Pool, which together interpret the DBAPI’s module functions as well as the behavior of the database.
  * **Dialect** names include the identifying name of the SQLAlchemy dialect, a name such as sqlite, mysql, postgresql, oracle, or mysql. 
  * A connection **pool** is a standard technique used to maintain long running connections in memory for efficient re-use, as well as to provide management for the total number of connections an application might use simultaneously.
  * **Database Urls:** Usually can include username, password, hostname, database name as well as optional keyword arguments for additional configuration. In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. The typical form of a database URL is:
    ```
    dialect+driver://username:password@host:port/database
    ``` 
  * In the simplest form we can consider the above as **connection string** which tell us what kind of database we are talking to & how we should access it. For the above code snippet we have used this connection string
    ```
    sqlite:////tmp/test.db
    ```
    **SQLite** (Database Driver) connects to file-based databases, using the Python built-in module sqlite3 by default. As SQLite connects to local files, the URL format is slightly different. The “file” portion of the URL is the filename of the database. 

    For a relative file path, this requires three slashes:
    ``sqlite://<nohostname>/<path>`` where ``<path>`` is relative

    For an absolute file path, the three slashes are followed by the absolute path. But for Unix/Mac - 4 initial slashes in total
    ``sqlite:////absolute/path/to/foo.db`` as used in the code snippet above ``sqlite:////tmp/test.db``

* The SQLAlchemy object **db** is created & the application is passed to it.

* Class Model is a declarative base which can be used to declare models. In the above code snippet:
  * The baseclass for all your models is called db.Model. 
  * **Column()** is used to define a column. The name of the column is the name you assign it to.
  * Primary keys are marked with primary_key=True. Multiple keys can be marked as primary keys in this case they become a compound primary key.
  * The types of the column are the first argument to Column. You can either provide them directly or call them to further specify them (like providing a length). The following types used in the above example are:
  * **Integer** is an Integer
  * **String(size)** a string with a maximum length
  * **unique** when true indicates that this column contains a unique constraint.
  * **nullable** when set to False will cause the "NOT NULL" phrase to be added when generating DDL for the column. When True, will normally generate nothing (in SQL this defaults to "NULL" 

* The \__repr__ is a dunder method also called a magic method. When you define a custom class in Python and then try to print one of its instances to the console (or inspect it in an interpreter session) you get a relatively unsatisfying result. The default “to string” conversion behavior is basic and lacking in detail. The solution here is adding the \__repr__ “dunder” method to your class. They are the Pythonic way to control how objects are converted to strings in different situations. The result of \__repr__ should be unambiguous.
The \__repr__ method above is used to return data in the database. It returns the data in the form of F-strings or Formatted Strings which 
provides a way to embed expressions inside string literals, using a minimal syntax.

# Run the App

* Debug Mode: Before running the App to enable all development features (including debug mode) you can export the FLASK_ENV environment variable using the terminal and set it to development before running the server:
  ```
  export FLASK_ENV=development
  flask run
  ```
 **Note:** This does the following things:
  * It activates the debugger
  * It activates the automatic reloader
  * It enables the debug mode on the Flask application
  
* To run this file using the terminal, use the command
   ```
   env FLASK_APP=test.py flask run
   ```
To run the application you can use the **flask** command. Before you can do that you need to tell your terminal the application to work with by exporting the **FLASK_APP** environment variable. The **FLASK_APP** environment variable is the name of the module to import at **flask run** or simply used to specify how to load the application. This launches a very simple builtin server, which is good enough for testing.
The **run** in flask run command will start the development server or run a local development server. It replaces the Flask.run() method in most cases.
  **Note:** You can also directly run using **python test.py**

* Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
  **Note:** Press CTRL+C to quit using the terminal

* To create the initial database, just import the db object from an **interactive Python shell** and run the **SQLAlchemy.create_all()** method to create the tables and database:
  ```
  >>> from test import db
  >>> db.create_all()
  ```
  Done, that's your database

* Now to create some users continuing with the **interactive python shell**:
  ```
  >>> from test import User
  >>> admin = User(username='admin', email='admin@example.com')
  >>> guest = User(username='guest', email='guest@example.com')
  ```

* The admin & the guest are not in the database yet, to make sure they are add them to the database using the **add()** to add it to the session & **commit()** to commit the session
  ```
  >>> db.session.add(admin)
  >>> db.session.add(guest)
  >>> db.session.commit()
  ```

* To access the data in the database
  ```
  >>> User.query.all()
      [User: admin, User: guest]
  >>> User.query.filter_by(username='admin').first()
      User: admin
  ```
The User.query.all() returns the results represented by this Query as a list.
The User.query.filter_by(username='admin').first() filters the data by the username='admin' & then returns the first result of this Query or None if the result doesn’t contain any row. first() applies a limit of one within the generated SQL, so that only one primary entity row is generated on the server side.

  **Note:** Move out of the interactive python shell by using the command **exit()**

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
  Or
  ```
  export FLASK_APP=run.py
  flask run
  ```

* Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser

  **Note:** Press CTRL+C to quit
