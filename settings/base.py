LOG_LEVEL = 'INFO'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

LOGGING_LEVELS_OVERRIDES = (
    # For local development.
    # Enable INFO log level for `tests` logger which is used by pytest tests.
    ('tests', 'INFO'),
)
