from threading import Lock

from Open_LISA_SDK.logging import log


def with_lock(lock: Lock):
    def decorator(method):
        def inner(ref, *args, **kwargs):
            lock.acquire()
            method_name = method.__name__
            log.debug('[with_lock][acquired][method={}]'.format(method_name))
            try:
                return method(ref, *args, **kwargs)
            finally:
                log.debug(
                    '[with_lock][released][method={}]'.format(method_name))
                lock.release()
        return inner

    return decorator
