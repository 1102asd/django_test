from django.db import models


class UnsignedAutoField(models.AutoField):
    """MySQL unsigned integer (range 0 to 4294967295)."""
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'


class UnsignedBigAutoField(models.BigAutoField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'bigint UNSIGNED AUTO_INCREMENT'
        else:
            # only support the 'sqlite'
            return 'integer'

    def rel_db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'bigint UNSIGNED'
        else:
            # only support the 'sqlite'
            return 'integer'


class UnsignedIntegerField(models.IntegerField):
    def db_type(self, connection):
        return 'integer UNSIGNED'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'


class UnsignedSmallIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        return 'smallint UNSIGNED'

    def rel_db_type(self, connection):
        return 'smallint UNSIGNED'


class UnsignedBigIntegerField(models.BigIntegerField):
    def db_type(self, connection):
        return 'bigint UNSIGNED'

    def rel_db_type(self, connection):
        return 'bigint UNSIGNED'
