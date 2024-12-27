
# 🛠️ Setting Up the Development Database

Follow these steps to set up the `dev-db` for your local environment! 🚀

---

## 📋 Prerequisites
Make sure you have the following installed:

- 📢 [Docker](https://www.docker.com/)
- 📢 [Docker Compose](https://docs.docker.com/compose/)

---

## 🏗️ Setup Instructions

1. **Navigate to the `dev-db` directory** 📂
   ```bash
   cd dev-db

2. **Run the `setup.sh` script** 📜:
   ```bash
   ./setup.sh<db-user> <db-password>
   ```
   Replace the placeholders with your desired database user and password.

   > 💡 The script will generate a `docker-compose.yml` file in the `dev-db` directory.

3. **Start the database** 🐳:
   ```bash
   docker compose up -d
   ```
---

## 🎉 You're all set!

- The database will be available at `localhost:8080` for Postgres and `localhost:8081` for MongoDB
- PgAdmin will be available at `localhost:5050` with `<db-user>@<repository-name>.com` and `<db-password>` as credentials
- Chroma will be available at `localhost:8082` with `<db-user>:<db-password>` as credentials. 
- The database files will be stored in the `<database-type>/data` directory.

---

## 📢 Troubleshooting

- If you encouter any issues, make sure Docker is properly running.
- You can check the logs by running:
  ```bash
  docker compose logs
  ```

