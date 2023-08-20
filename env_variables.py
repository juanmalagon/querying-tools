import os

# Define environment variables

# Change 'project_dir' to your project directory
os.environ['project_dir'] = '/Users/juanmalagon/repos/unbiased-request'

# Change 'scopus_config_file' to your Scopus config file. See:
# https://dev.elsevier.com/documentation/AuthenticationAPI
os.environ['scopus_config_file'] = os.path.join(
    os.getenv('project_dir'), 'scopus/config.json')

# Change 'scopus_data_dir' to your Scopus data directory:
# this is the place your Scopus retrieved data will be saved
os.environ['scopus_data_dir'] = os.path.join(
    os.getenv('project_dir'), 'data/')
os.environ['save_to_csv'] = '1'

# Change working directory
os.chdir(os.getenv('project_dir'))
