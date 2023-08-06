=====
ACL
=====

*Access control list (ACL) provides an additional, more flexible permission mechanism for file systems. It is designed to assist with UNIX file permissions. ACL allows you to give permissions for any user or group to any disc resource.*
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Use of ACL
----------

Think of a scenario in which a particular user is not a member of group
created by you but still you want to give some read or write access, how
can you do it without making user a member of group, here comes in
picture Access Control Lists, ACL helps us to do this trick.

Quick start
-----------

Add “django_acl” to your INSTALLED_APPS setting

.. code:: sh

   INSTALLED_APPS = [
           ...
           'django_acl',
       ]

Apply django-acl-permissions models

.. code:: sh

       python manage.py makemigrations
       python manage.py migrate

Add user_groups field in to your User Model

.. code:: sh

       class Users(AbstractBaseUser, PermissionsMixin):
           user_groups = models.ManyToManyField(
               Group,
               verbose_name=_("user_groups"),
               blank=True,
               help_text=_(
                   "The groups this user belongs to. A user will get all permissions "
                   "granted to each of their groups."
               ),
               related_name="user_set",
               related_query_name="user",
           )

Add has_acl_perms function in to your User Model

.. code:: sh

       def has_acl_perms(self, perm, obj = None):
           return _user_acl_has_perm(self, perm, obj=obj)


