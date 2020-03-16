# Database Environment Variables

To run the backend in other than `local` mode i.e `prod` or `develop` you need to export database environment variables.
These are the required database environment variables.
```
export DB_TYPE=<database_type>
export DB_USERNAME=<database_username>
export DB_PASSWORD=<database_password>
export DB_ENDPOINT=<database_endpoint>
export DB_NAME=<database_name>
```
 ## Database environment variables description


| Environment Variable | Description                                                                 | Example           |
|----------------------|-----------------------------------------------------------------------------|-------------------|
| DB_TYPE | Type of database you want to use | postgres, mysql
| DB_USERNAME          | Username of the user through which you will be doing operations in database | admin123, jhonDoe | 
| DB_PASSWORD | Database password of the `DB_USERNAME` user| admin@123, mypwd123|
| DB_ENDPOINT | Path to database or connection string connecting to database | /path/to/database.db |
| DB_Name | Name of the database to which you want to connect| Users.db, Tasks.db

## Exporting environment variables

Assume that KEY is the name of the variable and VALUE is the actual value of the environment variable. 
To export an environment variable you have to run:
```
export KEY=VALUE
```

- Example:
```
export DB_PASSWORD="admindb@123"
```

Another way to do this in flask applications is by having a file called `.env` which will have all of the environment variables. When a flask application runs, it will load these variables from the file.

- Content of `.env` file:

```
DB_PASSWORD="admindb@123"
DB_USERNAME="admin123"
(...)
```
