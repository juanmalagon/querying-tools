import os

# Define environment variables
os.environ['project_dir'] = '/Users/juanmalagon/repos/unbiased-request'
os.environ['scopus_config_file'] = os.path.join(
    os.getenv('project_dir'),
    'scopus/config.json'
    )
# Change working directory
os.chdir(os.getenv('project_dir'))
