===========
# payla_utils python package
===========


Features
--------

# Structlog config

## 1) Example, structlog configuration, django
in django settings.py

    from payla_utils.generic_logger.logger import GenericLogger

    logger = GenericLogger(
            service_name="your_service_name",
            default_level="INFO",
    ).configure_structlog()


## 2) If you want to use structlog in django celery

in celery.py

    from django.conf import settings
    from payla_utils.generic_logger.logger import GenericLogger

    @signals.setup_logging.connect
    def receiver_setup_logging(
        loglevel, logfile, format, colorize, **kwargs
    ):  # pragma: no cover

        logging.config.dictConfig(settings.LOGGING)

        logger = GenericLogger(
                service_name="your_service_name",
                default_level="INFO",
        ).configure_structlog()

## 3) If you want to use a structlog, not Django based project

    from payla_utils.generic_logger.logger import GenericLogger

    logger = GenericLogger(
            service_name="your_service_name",
            default_level="INFO",
            config=your_config,
            setup_logging_dict=True
    ).configure_structlog()


### 4) How to use generic structured logger:

    logger = structlog.get_logger(__name__)
    logger.warning("Here is your message", key_1="value_1", key_2="value_2", key_n="value_n")

### Why structured logger

- By default, the logging frameworks outputs the traces in plain text and tools like EFK stack or Grafana Loki can’t fully process these traces.
- Therefore, if we “structure” or send the traces in JSON format directly, all the tools can benefit of.
- As a developer, it would be nice to be able to filter all logs by a certain customer or transaction.
- The goal of structured logging is to solve these sorts of problems and allow additional analytics.


- When you log something, remember that the actual consumer is the machine Grafana Loki (EFK stack), not only humans.
- Our generic logger comes with some default context structure, but as you can see, you can introduce new keys.
- We use structlog as wraper on standard logging library, you can check for more details [structlog](https://www.structlog.org/en/stable/).
