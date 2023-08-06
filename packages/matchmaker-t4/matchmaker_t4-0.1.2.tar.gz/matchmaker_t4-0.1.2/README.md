# t4_matchmaker

This is the Matchmaker microservice for tabletoptournament.tools. It pairs players in event rounds according to the rules of the game they're playing.

Written for integration with the rest of the T4 software stack.

## Build the wheel

_Packaging and build references here: Packaging references here: https://packaging.python.org/en/latest/tutorials/packaging-projects/_

- Ensure `pyproject.toml` is up to date. Reference here: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
- Ensure you have python3.7+, pip and venv (`apt-get install python3-pip python3-venv`), and build (`pip3 install --upgrade build`) installed.
- Build the wheel
  `python3 -m build`

## Build and publish the server Docker image

- Move the wheel from ./dist/matchmaker-0.X.X-py3-none-any.whl into ./docker_setup/.
- Ensure `build.dockerfile` is updated, particularly ensuring MATCHMAKER_HASURA_ADMIN_SECRET, MATCHMAKER_HASURA_URL, and MATCHMAKER_DOMAIN are set correctly.
- From ./docker_setup/, build the Docker image.
  `docker build -t matchmaker:latest -f ./build.dockerfile .`
- Log Docker into AWS private ECR registry (requires AWS CLI configured and authorized for the private registry).
  `aws ecr get-login-password --region us-west-2 | docker login --username AWS \`
  `--password-stdin ACCT_ID_NUMBER.dkr.ecr.us-west-2.amazonaws.com`
- Push the Docker image to the private registry.
  `docker tag matchmaker:latest \`
  `ACCT_ID_NUMBER.dkr.ecr.us-west-2.amazonaws.com/matchmaker:latest`
  `docker push ACCT_ID_NUMBER.dkr.ecr.us-west-2.amazonaws.com/matchmaker:latest`
- Update Apprunner to pull the latest image. The dev environment is configured to automatically pull updates from the registry.
