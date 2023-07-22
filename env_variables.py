import os

# Define environment variables
os.environ['project_dir'] = '/Users/juanmalagon/repos/unbiased-request'
os.environ['scopus_config_file'] = os.path.join(
    os.getenv('project_dir'), 'scopus/config.json')
os.environ['scopus_data_dir'] = os.path.join(
    os.getenv('project_dir'), 'data/')
os.environ['save_to_csv'] = '1'

# Change working directory
os.chdir(os.getenv('project_dir'))
