# Simple Database Access Web Interface (SDAWI)

SDAWI allows you to work with different types of databases
through a web interface.

Supported database engines:
- PostgreSQL
- MySQL / MariaDB

Support for various databases is provided by [DBCW](https://github.com/Stefanitsky/dbcw)

## Installation and run

### pip

```bash
git clone https://github.com/Stefanitsky/sdawi.git
cd sdawi
pip install -r requirements.txt
python run sdawi.py
```

### pipenv
You must have [pipenv](https://github.com/pypa/pipenv) installed
```bash
git clone https://github.com/Stefanitsky/sdawi.git
cd sdawi
pipenv sync
pipenv run python sdawi.py
```

### Docker

You must have [Docker](https://docs.docker.com/install/) installed

##### Download via [DockerHub](https://hub.docker.com/r/stefanitsky/sdawi)
```bash
docker pull stefanitsky/sdawi
docker run --network host stefanitsky/sdawi
```

##### Or build from [source](https://github.com/Stefanitsky/sdawi/blob/master/Dockerfile)
```bash
git clone https://github.com/Stefanitsky/sdawi.git
cd sdawi
docker build -t sdawi .
docker run --network host sdawi
```

## Screenshots

| Description   | Screenshots   |
| ------------- | ------------- |
| Login page    | ![Login page](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/login_page.png) |
| Welcome page  | ![Welcome page](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/welcome_page.png) |
| Database page | ![Database page](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/database_structure_page.png) |
| Table page    | Structure tab:  ![Structure tab](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/table_structure_page.png)  Table data tab:  ![Table data tab](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/table_data_page.png) |
| SQL page      | Default: ![SQL page](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/sql_page.png)  Success query: ![Success query](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/sql_page_with_success_query.png)  Fail query: ![Success query](https://raw.githubusercontent.com/Stefanitsky/sdawi/docs/images/v0.2/sql_page_with_fail_query.png)|

These screenshots are from version 0.2  
[More screenshots in the docs branch](https://github.com/Stefanitsky/sdawi/tree/docs)

## Tests

#### Autotests

Work in progress

#### Manual tests

Via [docker-compose](https://docs.docker.com/compose/install/)
```bash
git clone https://github.com/Stefanitsky/sdawi.git
cd sdawi/tests
docker-compose up
```

## Contributing
Pull requests are welcome.
[TODO](https://github.com/Stefanitsky/sdawi/blob/master/TODO.md)

## License
[MIT](https://choosealicense.com/licenses/mit/)
