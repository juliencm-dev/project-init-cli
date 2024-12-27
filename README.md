# Installation Instructions

Follow these steps to set up your project-init script! 🚀

---

## 📋 Prerequisites
Make sure you have the following installed:

- Bash shell (if you use a different shell, you may need to modify the script)
- Git
- GitHub CLI
- Docker
- Docker Compose

---

## 🏗️ Setup Instructions

1. **Navigate to the `project-init` directory** 📂
   ```bash
   cd project-init
   ```

2. **Run the `install.sh` script** 📜:

- Make sure you have autorized the execution of the script:
  ```bash
   chmod +x install.sh
   ./install.sh
   ```
- This will create the alias `project-init` in your `~/.bashrc` file.
- It will also add 3 variables to your `~/.bashrc` file:
  - `PERSONAL_PATH`: The path to your personal projects.
  - `SCHOOL_PATH`: The path to your school projects. (Optional)
  - `GIT_USERNAME`: Your git username.

> 💡 You will setup the different paths during the installation process.

## 📜 Usage Instructions

You can now use the `project-init` script to create new projects!

### Arguments

The `project-init` script accepts the following arguments:

- `-h | -help`: Displays a help message with the available arguments.

- Mandatory arguments:
  - One of the following project type flags:
    - `-p`: Personal projects
    - `-s`: School projects (if you have school projects enabled)
  - `<repository-name>`: The name of the repository.

- Optional arguments:
   - `--db`: Comma-separated list of database types to setup
    - Options: postgres, mongodb, chroma
    - Example: --db postgres,mongodb
   - `[commit-message]`: The commit message for the initial commit
    - Default: "feat: `<repository-name>` initial commit"

### Example

To create a new personal project called `my-project` with a Postgres database and a commit message of "Initial commit", run:

```bash
project-init -p my-project --db postgres "Initial commit"
```

---

## 📢 Troubleshooting

- If you encouter any issues, make sure you have autorized the execution of the script.
- Contact me on [LinkedIn](https://www.linkedin.com/in/juliencm-dev/) or via email at [hello@juliencm.dev](mailto:hello@juliencm.dev) for any further assistance.
