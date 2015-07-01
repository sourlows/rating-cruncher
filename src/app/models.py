from google.appengine.ext import ndb

__author__ = 'djw'


class BaseModel(ndb.Model):
    KEY_NAME_FIELDS = []

    @classmethod
    def build_key_name(cls, **kwargs):
        """
        Builds the key_name for this model.
        raises ValueError if not KEY_NAME_FIELDS are provided.
        raises ValueError if a value for a KEY_NAME_FIELD is not provided.
        """
        if not cls.KEY_NAME_FIELDS:
            raise ValueError("No key name fields provided.")

        for field in cls.KEY_NAME_FIELDS:
            if field not in kwargs or not kwargs[field]:
                raise ValueError("%s is required" % field)

        return '-'.join([str(kwargs[field]).upper() for field in cls.KEY_NAME_FIELDS])

    @classmethod
    def build_key(cls, **kwargs):
        """ Builds a key in the default namespace. """
        key = ndb.model.Key(pairs=[(cls.__name__, cls.build_key_name(**kwargs))])
        return key