# unbiased-request
Repository accompanying the paper:

_Malagon J, Haelermans C. Reading between the lines: biases and reproducibility challenges in efficiency of education reviews. 2023_

### Instructions
1. On Python 3.11+ install the requirements:
`pip install -r requirements.txt`
2. Request your Elsevier API key at https://dev.elsevier.com/apikey/manage
3. Create a `config.json` file with your API key with contents
```
{
    "apikey": "your_api_key_goes_here"
}
```
(See also
Elsevier Developer Portal API Authentication docs https://dev.elsevier.com/tecdoc_api_authentication.html
API Interface Specification https://dev.elsevier.com/documentation/AuthenticationAPI)

4. Store your `config.json` file at the `/scopus/` folder
5. Open `env_variables.py` and change `project_dir` to your current project directory
6. Open a terminal and run
`streamlit run unbiased_requester.py`
