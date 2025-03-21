"""
helper file to keep the code
that seems good enough to be here

    - validate_env_vars

"""
import os


REQUIRED_VARS = ['API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_SECRET', 'BEARER_TOKEN']


def validate_env_vars():
    missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")