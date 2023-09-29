import os

class Config(object):
    """
    Base configuration class. Contains default settings that will be inherited by all the other configuration subclasses.
    """
    DEBUG = False  # Turn off debugging by default
    TESTING = False  # Turn off testing by default
    CSRF_ENABLED = True  # Enable CSRF protection by default
    SECRET_KEY = 'my_coding_challenge'  # Define a secret key.


class ProductionConfig(Config):
    """
    Production configuration. Inherits from the base configuration and overrides specific settings.
    """
    DEBUG = False  # Ensure that debugging is turned off in production


class StagingConfig(Config):
    """
    Staging configuration. Inherits from the base configuration and overrides specific settings.
    """
    DEVELOPMENT = True  # Staging mimics a production environment, but is still in development
    DEBUG = True  # Debugging is enabled in the staging environment


class DevelopmentConfig(Config):
    """
    Development configuration. Inherits from the base configuration and overrides specific settings.
    """
    DEVELOPMENT = True  # Development environment
    DEBUG = True  # Debugging is enabled in development


class TestingConfig(Config):
    """
    Testing configuration. Inherits from the base configuration and overrides specific settings.
    """
    TESTING = True  # Enable testing mode
