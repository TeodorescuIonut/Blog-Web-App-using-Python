from functools import wraps
from services.service import ContainerService


def injector(func):
    @wraps(func)
    def wrapper_services(*args, **kwargs):
        arguments: list = []
        services = ContainerService.get_service()
        annotations = func.__annotations__
        service_types = annotations.values()
        for annotation in annotations:
            for service in services:
                if annotation == "return":
                    continue
                if service in service_types:
                    arguments.append(services[service])
            return func(*arguments, *args, **kwargs)
    return wrapper_services
