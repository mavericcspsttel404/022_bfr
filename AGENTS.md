# Contributor Guide

## Some project specific context and rules

- We only use Microsoft sql server as our database so write logic adn tests accordingly.
- For Salesforce use simpleSalesforce library.
- Try to use SOLID principles as much as possible.

## Dev Environment Tips

- Make sure all the types are properly mentioned for all parameters.
- Use "ruff check" to check for any issues.

## Testing Instructions

- From the package root you can just call "pytest".
- The commit should pass all tests before you merge.
- Fix any test or type errors until the whole suite is green.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions

- Make sure to add/modify relevant tests to ensure code coverage.
- Make sure all tests pass before sending a PR.
