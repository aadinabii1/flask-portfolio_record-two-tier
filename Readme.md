# 🧩 Flask Portfolio Records Application

A simple **two-tier web application** built using **Flask** (frontend) and **MySQL** (backend database).
This project is designed for **DevOps practice**, demonstrating containerization, environment-based configuration, and Docker networking.

---

## 🚀 Overview

The application allows users to:

* Add their portfolio details (Name, Role, Skills, and Email)
* Store those records in a MySQL database
* View all submissions in a responsive HTML table

It’s lightweight and designed to teach:

* How applications communicate inside Docker networks
* How environment variables are used for configuration
* How to containerize and deploy simple web stacks

---

## 🏗️ Architecture

```
                     +----------------------+
                     |   Flask Application  |
                     |----------------------|
   HTTP :8080  --->  |  Renders HTML Forms  |
                     |  Connects to MySQL   |
                     +----------+-----------+
                                |
                                | Docker Bridge Network (app-tier)
                                |
                     +----------+-----------+
                     |     MySQL Database   |
                     |----------------------|
                     | Stores portfolio data|
                     +----------------------+
```

---

## ⚙️ Tech Stack

| Component        | Technology                       |
| ---------------- | -------------------------------- |
| Frontend / API   | Flask (Python)                   |
| Backend          | MySQL                            |
| Language         | Python 3                         |
| Containerization | Docker                           |
| Networking       | User-defined bridge (`adnan-isolated-network`) |

---

## 📁 Project Structure

```
flask-portfolio/
│
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Flask container definition
├── templates/
│   ├── form.html          # Form page (Add portfolio)
│   └── table.html         # Table view (View portfolios)
└── README.md              # This file
```

---

## 🔧 Configuration

The Flask app reads **all configuration values from environment variables**.
You must provide these variables when running the container, either individually with `-e` or through an `.env` file.

| Variable      | Description                         | Default                               |
| ------------- | ----------------------------------- | ------------------------------------- |
| `DB_HOST`     | Database hostname or container name | `db`                                  |
| `DB_USER`     | MySQL username                      | `appuser`                             |
| `DB_PASSWORD` | MySQL user password                 | `app123`                              |
| `DB_NAME`     | MySQL database name                 | `app_db`                              |
| `DB_PORT`     | MySQL port                          | `3306`                                |
| `SECRET_KEY`  | Flask secret key                    | `dev-secret-key-change-in-production` |
| `PORT`        | Flask port inside container         | `5000`                                |
| `DEBUG`       | Flask debug mode                    | `False`                               |

Example `.env` file:

```
SECRET_KEY=my-secret-key
DB_HOST=db
DB_USER=appuser
DB_PASSWORD=app123
DB_NAME=app_db
DB_PORT=3306
PORT=5000
DEBUG=False
```

---

## 🐳 Running with Docker

### 1. Create a Docker network

```bash
docker network create adnan-isolated-network
```

### 2. Start MySQL

```bash
docker run -d \
--name db \
--network adnan-isolated-network \
-e MYSQL_ROOT_PASSWORD=root \
-e MYSQL_DATABASE=portfolio \
-e MYSQL_USER=adnan \
-e MYSQL_PASSWORD=adnan \
mysql:8
```

### 3. Initialize the table

```bash
docker exec -i db mysql -uadnan -padnan portfolio -e "CREATE TABLE IF NOT EXISTS portfolio (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), role VARCHAR(100), skills TEXT, email VARCHAR(100));"
```

### 4. Build the Flask image

```bash
docker build -t flask-portfolio-two-tier .
```

### 5. Run the Flask app container

**Option A: Using an `.env` file (recommended)**

```bash
docker run -d \
  --name app \
  --network adnan-isolated-network \
  --env-file .env \
  -p 8080:5000 \
  flask-portfolio-two-tier
```

**Option B: Passing environment variables directly**

```bash
docker run -d \
  --name app \
  --network adnan-isolated-network \
  -e DB_HOST=db \
  -e DB_USER=adnan \
  -e DB_PASSWORD=adnan \
  -e DB_NAME=portfolio \
  -e SECRET_KEY=adnan123 \
  -e DEBUG=False \
  -p 8080:5000 \
  adnannabi/flask-portfolio-two-tier
```

### 6. Access the application

Visit:
👉 [http://localhost:8080](http://localhost:8080)

---

## 📦 Local Requirements (if running without Docker)

```
flask==3.0.3
mysql-connector-python==9.0.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python app.py
```

---

## 💡 Features

* Responsive HTML interface (form + table)
* Flash message alerts for success and error feedback
* Environment-based configuration (no hardcoded values)
* Clean Docker setup (small image, no unnecessary layers)
* Works out of the box with MySQL 8

---

## 🧠 DevOps Concepts Demonstrated

| Concept                      | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| **Containerization**         | Flask and MySQL run as isolated containers               |
| **Networking**               | Uses Docker user-defined bridge network(`adnan-isolated`)|
| **Configuration Management** | Fully driven by environment variables                    |
| **Port Mapping**             | Host port 8080 → Container port 5000                     |
| **Image Optimization**       | `python:slim` base, `--no-cache-dir` pip install         |
| **Security Practice**        | Secret key and DB creds passed via environment variables |

---

## ✨ Author

**Adnan**
*Network Engineer | Aspiring DevOps Engineer*
Building strong foundations in Docker, Kubernetes, CI/CD, and Cloud — one hands-on project at a time.
