# 🧩 Flask Portfolio Records Application

A simple **two-tier web application** built using **Flask** (frontend) and **MySQL** (backend database).
This project is created for **DevOps hands-on practice**, demonstrating **containerization**, **networking**, and **environment-based configuration** with Docker.

---

## 🚀 Overview

The application allows users to:

* Add portfolio details (Name, Role, Skills, Email)
* Store data in a MySQL database
* View all entries in a responsive HTML table

This project helps understand:

* How containers communicate in Docker networks
* How to use environment variables for app configuration
* How to containerize and deploy multi-tier apps

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
                                | Docker Bridge Network (adnan-isolated-network)
                                |
                     +----------+-----------+
                     |     MySQL Database   |
                     |----------------------|
                     | Stores portfolio data|
                     +----------------------+
```

---

## ⚙️ Tech Stack

| Component        | Technology                                     |
| ---------------- | ---------------------------------------------- |
| Frontend / API   | Flask (Python)                                 |
| Backend          | MySQL 8                                        |
| Language         | Python 3                                       |
| Containerization | Docker                                         |
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
├── init.sql               # MySQL table initialization
├── docker-compose.yml     # Two-tier app setup (Flask + MySQL)
└── README.md              # This file
```

---

## 🔧 Configuration

The Flask app reads **all configuration values** from environment variables.

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

### Example `.env` file

```bash
SECRET_KEY=my-secret-key
DB_HOST=db
DB_USER=adnan
DB_PASSWORD=adnan
DB_NAME=portfolio
DB_PORT=3306
PORT=5000
DEBUG=False
```

---

## 🐳 Running with Docker Compose

Bring up both containers (MySQL + Flask) in one go:

```bash
docker compose up --build
```

Access the app at 👉 [http://localhost:8080](http://localhost:8080)

---

## 🧱 Running Manually (Without Compose)

If you want to practice networking and linking manually:

### 1. Create a Docker network

```bash
docker network create adnan-isolated-network
```

### 2. Start the MySQL container

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

### 3. Initialize the MySQL table

```bash
docker exec -i db mysql -uadnan -padnan portfolio -e \
"CREATE TABLE IF NOT EXISTS portfolio (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), role VARCHAR(100), skills TEXT, email VARCHAR(100));"
```

### 4. Build the Flask app image

```bash
docker build -t flask-portfolio-two-tier .
```

### 5. Run the Flask container

**Option A: Using `.env` file**

```bash
docker run -d \
  --name app \
  --network adnan-isolated-network \
  --env-file .env \
  -p 8080:5000 \
  flask-portfolio-two-tier
```

**Option B: Without `.env` file (pass variables directly)**

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
  flask-portfolio-two-tier
```

---

## 💡 Features

* Responsive HTML (form + table)
* Flash messages for success/error
* Environment-based configuration
* Health checks for both Flask and MySQL
* Persistent MySQL storage (via volumes)
* Lightweight image using `python:3.12-slim`

---

## 🧠 DevOps Concepts Demonstrated

| Concept                | Description                                     |
| ---------------------- | ----------------------------------------------- |
| **Containerization**   | Flask and MySQL run in isolated containers      |
| **Networking**         | Custom bridge network for service communication |
| **Configuration**      | Managed via environment variables               |
| **Health Checks**      | Ensure MySQL is ready before Flask starts       |
| **Volumes**            | Data persistence across container restarts      |
| **Image Optimization** | Uses slim image, minimal layers                 |
| **Restart Policy**     | Services auto-restart if stopped unexpectedly   |

---

## ✨ Author

**Adnan**
*Network Engineer → Aspiring DevOps Engineer*
Building strong foundations in **Docker, Kubernetes, CI/CD, and Cloud** — one hands-on project at a time.
