from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


class PublishService():
    def __init__(self, settings=settings):
        self._publish_providers = []
        self._initialised = False
        self.settings = settings
    
    def _manual_init(self):
        """Manual init had to be called by all the functions of the PublishService
        class to initialise the instance variables. This block of code used to
        be in the __init__ function but has been moved to its own init function
        to get around the problems with cyclic imports to static variables
        being exported from auth related modules.
        
        """
        for pp in self.settings.PUBLISH_PROVIDERS:
            self._publish_providers.append(self._safe_import(pp))
        self._initialised = True
    
    def _safe_import(self, path):
        try:
            dot = path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured('%s isn\'t a middleware module' % path)
        publish_module, publish_classname = path[:dot], path[dot + 1:]
        try:
            mod = import_module(publish_module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing publish module %s: "%s"' %
                                       (publish_module, e))
        try:
            publish_class = getattr(mod, publish_classname)
        except AttributeError:
            raise ImproperlyConfigured('Publish module "%s" does not define a "%s" class' %
                                       (publish_module, publish_classname))
        
        publish_instance = publish_class()
        return publish_instance
    
    def get_publishers(self):
        """Return a list of tuples containing publish plugin name
        
        """
        if not self._initialised:
            self._manual_init()
        publicaton_list = []
        for pp in self._publish_providers:
            # logger.debug("group provider: " + gp.name)
            publicaton_list.append(pp.name)
        return publicaton_list
    
    def get_template_paths(self):
        """Return a list of tuples containing publish plugin name
        
        """
        if not self._initialised:
            self._manual_init()
        path_list = []
        for pp in self._publish_providers:
            # logger.debug("group provider: " + gp.name)
            path_list.append(pp.get_template_path())
        return path_list        