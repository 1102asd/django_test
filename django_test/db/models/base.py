from django.db import models

from django_user.authentication import _auth_ctx

from .deletion import on_delete_handler, ModelOnDeleteMixin
from django_test.db.models.fields import (
    UnsignedBigIntegerField,
)


def current_user_id():
    if hasattr(_auth_ctx, 'user'):
        return _auth_ctx.user.userprofile.id
    else:
        return 0


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        qs = SoftDeleteQuerySet(self.model, using=self._db)
        return qs.filter(is_deleted=False)


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        on_delete_handler(self)
        return self.update(is_deleted=True)

    def update(self, **kwargs):
        return super(SoftDeleteQuerySet, self).update(update_user_id=current_user_id(), **kwargs)


class AllQueryManager(models.Manager):
    def get_queryset(self):
        return super(AllQueryManager, self).get_queryset()


class BaseModel(ModelOnDeleteMixin, models.Model):
    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    objects_all = AllQueryManager()

    create_time = models.DateTimeField(db_column='create_time', auto_now_add=True)
    update_time = models.DateTimeField(db_column='update_time', auto_now=True)
    create_user_id = UnsignedBigIntegerField(verbose_name='创建人 ID', default=current_user_id)
    update_user_id = UnsignedBigIntegerField(verbose_name='更新人 ID', default=0)
    is_deleted = models.BooleanField(verbose_name="是否已删除", default=False, help_text='删除标志')
    note = models.CharField(verbose_name="备注", max_length=512, default='', null=True)

    BASE_FIELDS = ('create_time', 'update_time', 'create_user_id', 'update_user_id', 'is_deleted', 'note')

    def delete(self):
        self.on_delete()
        self.is_deleted = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        current_uid = current_user_id()
        if current_uid != 0:
            self.update_user_id = current_uid
        return super().save(force_insert, force_update, using, update_fields)


class BaseHardModel(ModelOnDeleteMixin, models.Model):
    """特殊的关联关系，比如多对多 mapping、一对一需要建立唯一索引等情况，根据实际场景，可以考虑硬删除
    一般来说，这类表是 API 内部业务维护的逻辑，不应该有用户直接接触此表数据。
    """
    class Meta:
        abstract = True

    create_time = models.DateTimeField(db_column='create_time', auto_now_add=True)
    update_time = models.DateTimeField(db_column='update_time', auto_now=True)
    create_user_id = UnsignedBigIntegerField(verbose_name='创建人 ID', default=current_user_id)
    update_user_id = UnsignedBigIntegerField(verbose_name='更新人 ID', default=0)

    def delete(self):
        self.on_delete()
        super().delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.update_user_id = current_user_id()
        return super().save(force_insert, force_update, using, update_fields)
