import errno
import logging
import os


def overwrite_or_merge(target_dict: dict, source_dict: dict, path=None):
    "merges b into a"
    if path is None:
        path = []

    for key in source_dict:
        if key in target_dict:
            if isinstance(target_dict[key], dict) and isinstance(source_dict[key], dict):
                overwrite_or_merge(target_dict[key], source_dict[key], path + [str(key)])
            else:
                target_dict[key] = source_dict[key]  # overwriting value in a by value in b
        else:
            target_dict[key] = source_dict[key]
    return target_dict


msg_only_formatter = logging.Formatter('%(message)s')
handler_dic = {}


def setup_logger(name, log_file, level=logging.INFO, logging_format=True, msg_only=False, log_rotation_unit='h',
                 log_rotation_interval=4):
    from logging import handlers
    """Function setup as many loggers as you want"""
    create_dir_if_not_exists(log_file)
    handler = handler_dic.get(log_file)
    if not handler:
        handler = handlers.TimedRotatingFileHandler(log_file, when=log_rotation_unit, interval=log_rotation_interval)
        handler_dic[log_file] = handler

    if logging_format:
        if msg_only:
            handler.setFormatter(msg_only_formatter)
        else:
            timed_log_formatter = logging.Formatter(f'{name}:%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(timed_log_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def create_dir_if_not_exists(file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)


def delete_file_silently(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT: no such file or directory
            raise e
