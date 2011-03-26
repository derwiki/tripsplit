def ajax(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                res.setdefault('success', True)
                return json.dumps(res)
            except Exception, e:
                log.error(traceback.format_exc())
                log.error(e)
                return json.dumps(dict(sucess=False, error=str(e)))
        return wrapper
    return decorator

