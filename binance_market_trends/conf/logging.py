from pythonjsonlogger import jsonlogger

from binance_market_trends.conf.settings import settings, Env


class BaseJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(BaseJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name


class GunicornUvicornJsonFormatter(BaseJsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(GunicornUvicornJsonFormatter, self).add_fields(log_record, record, message_dict)

        if 'scope' in log_record:
            del log_record['scope']


log_level = settings.LOG_LEVEL.value


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': BaseJsonFormatter,
        },
        'gunicorn_uvicorn_json': {
            '()': GunicornUvicornJsonFormatter,
        },
        'local': {
            '()': 'logging.Formatter',
        }
    },
    'handlers': {
        'default': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'gunicorn_uvicorn': {
            'formatter': 'local' if settings.ENV == Env.LOCAL else 'gunicorn_uvicorn_json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'binance_market_trends': {'handlers': ['default'], 'level': log_level},
        'uvicorn': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn.access': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
        'gunicorn.error': {'handlers': ['gunicorn_uvicorn'], 'level': log_level},
    },
    'root': {'handlers': ['default'], 'level': log_level}
}
