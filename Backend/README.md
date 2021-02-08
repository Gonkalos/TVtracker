# Server

A Flask-driven RESTful API.

---

## Table Of Contents

- [Tecnologies Used](#Technologies-Used)
- [Getting Started](#Getting-Started)
  - [Instalation](#Installation)
  - [Configuration](#Configuration)
- [How To Use](#How-To-Use)
  - [Compile And Run](#Compile-And-Run)
  - [API Documentation](#API-Documentation)


---

## Technologies Used

- [Python](https://www.python.org) - A programming language that lets you work quickly and integrate systems more effectively.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - A Python microframework based on the Pocoo projects, Werkzeug and Jinja2.
- [MySQL](https://www.mysql.com) - A freely available open source Relational Database Management System that uses Structured Query Language (SQL).
- [JSON Web Tokens](https://jwt.io) (JWT) - An open, industry standard RFC 7519 method for representing claims securely between two parties.
- [OMDb API](http://www.omdbapi.com) - A RESTful web service to obtain movies and TV series information.

---

## Getting Started

### Installation

- Ensure that you have the latest versions of Python3 and MySQL globally installed in your computer.

> If you are running macOS, make sure to set Python3 and pip3 as default.

- To install all dependencies go to `/Utils` and run the following command:
```
pip install -r requirements.txt
```

### Configuration

The server is configured via the `configs.py` file. Create this file in `/Utils` with the following syntax:

```
# OMDb API
OMDB_API_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = 'your-OMDb-key'

# MySQL Database
DB_USERNAME = 'your-MySQL-username' 
DB_PASSWORD = 'your-MySQL-user-password'
DB_NAME = 'your-MySQL-database-name'

# JWT Authentication
JWT_SECRET_KEY = 'your-JWT-secret-key'
JWT_ALGORITHM = 'your-preferred-JWT-algorithm'
```
> To generate a JWT secret key go to `/Utils` and run the following command:
```
python secretKey.py
```
---

## How To Use

### Compile And Run

To start the server simply run the following command:
```
sh start.sh
```

### API Documentation

<details>
  <summary> Create an account </summary>
  <p>

   ```
   POST http://127.0.0.1:5000/CreateAccount
   Authorization: None
   Content-Type: application/json 
   Accept: text/html
   Accept-Charset: charset=utf-8
   ```

   Body fields:

   | Field | Type | Description |
   |-------|------|-------------|
   | username | string | Account username |
   | email | string | Account email |
   | password1 | string | Account password (first entry) |
   | password2 | string | Account password (second entry) |

  </p>
</details>

<details>
  <summary> Login </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/Login
  Authorization: None
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | email | string | Account email |
  | password | string | Account password |

  </p>
</details>

<details>
  <summary> Change Password </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/ChangePassword
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | old_password | string | Account password |
  | new_password1 | string | Account new password (first entry) |
  | new_password2 | string | Account new password (second entry) |

  </p>
</details>

<details>
  <summary> Search Series </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/SearchSeries
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | search | string | Series title |

  </p>
</details>

<details>
  <summary> Get Series </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/GetSeries
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | imdbID | string | Series IMDb id |

  </p>
</details>

<details>
  <summary> Add Series </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/AddSeries
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | imdbID | string | Series IMDb id |

  </p>
</details>

<details>
  <summary> Remove Series </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/Remove
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | imdbID | string | Series IMDb id |

  </p>
</details>

<details>
  <summary> Update Series Status </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/UpdateSeriesStatus
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Valid Options | Description |
  |-------|------|---------------|-------------|
  | imdbID | string | | Series IMDb id |
  | status | string | Watching, Rewatching, Completed, Plan To Watch | Series updated status |

  </p>
</details>

<details>
  <summary> Check Episode </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/CheckEpisode
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | imdbID | string | Series IMDb id |

  </p>
</details>

<details>
  <summary> Update Episodes </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/UpdateEpisodes
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Description |
  |-------|------|-------------|
  | imdbID | string | Series IMDb id |
  | updated_episode | integer | Last episode seen |
  | updated_season | integer | Season of the last episode seen |

  </p>
</details>

<details>
  <summary> Rate Series </summary>
  <p>

  ```
  POST http://127.0.0.1:5000/RateSeries
  Authorization: Bearer Token
  Content-Type: application/json
  Accept: text/html
  Accept-Charset: charset=utf-8
  ```

  Body fields:

  | Field | Type | Valid Options | Description |
  |-------|------|---------------|-------------|
  | imdbID | string | | Series IMDb id |
  | rating | integer | 1, 2, 3, 4, 5 | Series rating |

  </p>
</details>

> Please note that for each request all fields are required.

<details>
  <summary> Errors </summary>
  <p>

  This server uses conventional HTTP response codes to indicate the success or failure of an API request. 
  - Codes in the 2xx range indicate success
  - Codes in the 4xx range indicate an error that failed given the information provided
  - Codes in the 5xx range indicate an error with the server

  | Status Code | Meaning | Description |
  |-------------|---------|-------------|
  | 200 | OK | Everything worked as expected. |
  | 400 | Bad Request | The request was unacceptable, often due to missing a required parameter. |
  | 401 | Unauthorized | The request requires user authentication. |
  | 404 | Not Found | The requested resource doesn't exist. |
  | 500 | Internal Server Error | The server encountered an unexpected condition which prevented it from fulfilling the request. |
  | 502 | Bad Gateway | The server received an invalid response from the OMDb API. |
  
  </p>
</details>
