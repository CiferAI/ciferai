# Contributing to Cifer

We welcome all contributions to push forward Privacy-Preserving Machine Learning through Federated Learning and Fully Homomorphic Encryption 

## Legal Notice
All contributions to CiferAI will be licensed under the Apache License, Version 2.0. By contributing, you agree that your contributions will be covered by this license.

***Key Takeaways of Apache License 2.0***
1. **Usage Rights:** Grants users the freedom to use, modify, distribute, and sublicense the software for any purpose, including commercial use.
2. **Attribution:** Requires retention of copyright notices and attribution to original authors in all copies or substantial portions of the software.
3. **Patent Grant:** Provides an express grant of patent rights from contributors to users.
4. **Trademark Use:** Does not grant permission to use the trademarks of contributors.
5. **No Warranty:** Software is provided "as is" without warranties or conditions of any kind.
6. **Limitation of Liability:** Contributors are not liable for damages arising from the use of the software.
7. **License and Notice:** Requires inclusion of a copy of the license and any notices in redistributions.
8. **Contributions:** Submissions intentionally for inclusion are deemed to be under the same license.
9. **Derivative Works:** Allows creation of derivative works, but requires clear indication of changes made.

## Code of Conduct
CiferAI is committed to fostering an open, inclusive, and respectful community. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) as our Code of Conduct. All contributors are expected to uphold these standards. Please refer to our [CODE_OF_CONDUCT](https://github.com/CiferAI/ciferai/blob/main/CODE_OF_CONDUCT.md) for more information.

## Contribution Guidelines
To contribute, simply fork our repository and submit a Pull Request on GitHub. All contributions, whether from community members or core maintainers, must undergo code review. Ensure that your changes pass our Continuous Integration (CI) checks. A project maintainer will review your Pull Request, and upon approval, it will be merged into the main branch.

## Code Review and Acceptance
All contributions will go through a thorough code review to maintain the highest standards of quality, security, and privacy. Reviews will assess the following:
1. **Code Quality:** Your code should follow best practices in readability, structure, and efficiency. We encourage the use of comments where necessary, especially for complex sections.
2. **Testing:** Please ensure your contribution includes appropriate tests. This helps us ensure that new features work as expected and that existing functionality remains intact. If adding new functionality, include unit tests and verify that all tests pass before submitting a pull request.
3. **Documentation:** All new features or significant changes should be documented in the relevant documentation files. Ensure the README.md is updated if your change affects the installation, usage, or API. If you contribute a new feature, consider adding an example that demonstrates its usage.
4. **Security and Privacy:** Since Cifer focuses on privacy-preserving machine learning, we ask contributors to be especially vigilant about maintaining privacy and security standards. Contributions related to federated learning or fully homomorphic encryption should take extra care to ensure the privacy of user data is preserved.

## Contribution Process
1. **Fork the Repository:** First, fork the main repository to create your own copy.
2. **Create a New Branch:** Create a new branch in your fork for your changes. For example:
```
git checkout -b feature/new-feature
```
3. **Make Your Changes:** Implement your changes in your branch, ensuring that you adhere to the coding standards and have added tests/documentation as required.
4. **Run Tests:** Run the tests locally to ensure everything works as expected:
```
pytest
```
5. **Submit a Pull Request:** Once your changes are ready, push them to your fork and submit a pull request (PR) to the main repository. Include a clear description of the changes you've made, the problem it solves, or the feature it introduces. If relevant, link to any related issues.
6. **Code Review:** Your PR will be reviewed by one or more maintainers. They may request changes or ask clarifying questions. Once the review is complete and the necessary changes (if any) have been made, your PR will be merged.

## Data Handling with Git LFS

Due to the large size of the datasets and dynamic libraries (e.g., `.dylib` files) used with Cifer, we utilize **Git Large File Storage (LFS)** to manage these large files efficiently. Git LFS ensures that large files are stored outside of this Git repository while maintaining references to them in the repository.

To set up Git LFS for this repository, follow these steps:

1. **Install Git LFS** on your local machine:

    ```bash
    git lfs install
    ```

2. **Track large file types** such as dataset images and dynamic libraries by specifying file extensions:

    ```bash
    git lfs track "*.jpg"
    git lfs track "*.png"
    git lfs track "*.dylib"
    ```

3. **Stage the `.gitattributes` file** created by Git LFS and your large files:

    ```bash
    git add .gitattributes
    git add <path-to-large-files>
    ```

4. **Commit your changes** to the repository:

    ```bash
    git commit -m "Add large files with Git LFS"
    ```

5. **Push to this repository**:

    ```bash
    git push origin main
    ```

This workflow ensures that large files are efficiently managed and versioned without bloating this repository.

## Thank You
We’re grateful for your time and effort in contributing to CiferAI! Together, we can push the boundaries of decentralized machine learning and fully homomorphic encryption.
