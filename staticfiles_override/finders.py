import os.path
import re

from django.contrib.staticfiles import finders
from django.conf import settings


class StorageOverride:
    def __init__(self, storage, name, prefix=None):
        self.storage = storage
        self.name = name
        if prefix is not None:
            self.prefix = prefix

    def open(self, name, mode='rb', mixin=None):
        return self.storage.open(self.name, mode=mode, mixin=mixin)

    def save(self, name, content):
        return self.storage.save(self.name, content)

    def get_valid_name(self, name):
        return self.storage.get_valid_name(self.name)

    def get_available_name(self, name):
        return self.storage.get_available_name(self.name)

    def path(self, name):
        return self.storage.path(self.name)

    def delete(self, name):
        return self.storage.delete(self.name)

    def exists(self, name):
        return self.storage.exists(self.name)

    def listdir(self, path):
        return self.storage.listdir(path)

    def size(self, name):
        return self.storage.size(self.name)

    def url(self, name):
        return self.storage.url(self.name)

    def accessed_time(self, name):
        return self.storage.accessed_time(self.name)

    def created_time(self, name):
        return self.storage.created_time(self.name)

    def modified_time(self, name):
        return self.storage.modified_time(self.name)


class AppDirectoriesFinder(finders.AppDirectoriesFinder):
    def __init__(self, apps=None, overrides=None, *args, **kwargs):
        super(AppDirectoriesFinder, self).__init__(apps=apps, *args, **kwargs)
        if overrides is None:
            try:
                overrides = settings.STATICFILES_OVERRIDES
            except AttributeError:
                overrides = {}
        self.overrides = overrides

    def _override_path(self, path):
        if self.overrides:
            for pat, repl in self.overrides.items():
                new_path, replaced = re.subn(pat, repl, path)
                if replaced:
                    return new_path

    def _get_storage_for_path(self, path):
        for finder in finders.get_finders():
            try:
                storages = finder.storages.itervalues()
            except AttributeError:
                try:
                    storages = [finder.storage]
                except AttributeError:
                    storages = []

            for storage in storages:
                try:
                    prefix = '%s%s' % (storage.prefix, os.sep)
                except AttributeError:
                    pass
                else:
                    if not path.startswith(prefix):
                        continue

                if storage.exists(path):
                    return storage

    def find(self, path, all=False):
        new_path = self._override_path(path)
        result = None
        if new_path:
            result = finders.find(new_path, all=all)

        if not result:
            result = super(AppDirectoriesFinder, self).find(path, all=all)

        return result

    def list(self, ignore_patterns):
        result = super(AppDirectoriesFinder, self).list(ignore_patterns)

        new_result = []
        for path, storage in result:
            if getattr(storage, 'prefix', None):
                prefixed_path = os.path.join(storage.prefix, path)
            else:
                prefixed_path = path

            new_path = self._override_path(prefixed_path)

            if new_path is None:
                new_result.append((path, storage))
            else:
                new_storage = self._get_storage_for_path(new_path)

                if new_storage is None:
                    # Override does not exist, fallback to original
                    new_result.append((path, storage))
                else:
                    new_storage = StorageOverride(new_storage, new_path,
                                                  getattr(storage, 'prefix', None))
                    new_result.append((path, new_storage))

        return new_result
