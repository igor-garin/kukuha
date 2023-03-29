import logging
import logging.config

import settings


def _init_logger():
    logging_config = settings.LOGGING_CONFIG
    logging_config['loggers']['']['level'] = settings.LOG_LEVEL

    for name, level in settings.LOGGING_LEVELS_OVERRIDES:
        logging_config['loggers'][name] = {
            'level': level,
        }

    logging.config.dictConfig(logging_config)
