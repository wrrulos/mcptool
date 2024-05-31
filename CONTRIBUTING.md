# Contribution Guide

Thank you for your interest in contributing to **mcptool**! Below are some ways you can help improve this project.

## Report problems or suggestions

If you find a bug or have a suggestion to improve the project, please open an [issue](https://github.com/wrrulos/mcptool/issues) on GitHub.

If you have an idea for a new feature, open an [issue](https://github.com/wrrulos/mcptool/issues) and tag it "feature request". Describe in detail how you would like the new functionality to work.

## Pull requests

1. **Fork the repository** – Click the “Fork” button at the top right of the repository page. This will create a copy of the project in your GitHub account.

2. **Clone your fork** - Clone your repository using the command and go to the folder.

    ```sh
    git clone https://github.com/youruser/mcptool.git
    cd mcptool
    ```

3. **Create a new branch** - Create a new branch for your changes. (Do not work directly on the main branch)

    ```sh
    git checkout -b branch-name
    ```

4. **Make your changes** - Make the necessary changes in your branch. Make sure you follow the code guidelines.

5. **Sync your fork with the original repository** - If the original repository has had changes since you forked it, it is good practice to sync your fork before uploading the changes.

    ```sh
    git remote add upstream https://github.com/wrrulos/mcptool.git
    git fetch upstream
    git merge upstream/main
    ```

6. **Upload your changes** - Upload your branch to your fork repository on GitHub.

    ```sh
    git push origin branch-name
    ```

7. **Abre un Pull Request** - Go to your fork page on GitHub and click “New Pull Request.” Choose the master branch of the original repository as the base and its branch as the comparison branch. Be sure to provide a clear title and detailed description of your changes in the pull request.

