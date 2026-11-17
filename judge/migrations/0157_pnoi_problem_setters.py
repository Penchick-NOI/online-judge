from django.contrib.auth.management import create_permissions
from django.db import migrations

GROUP = 'Problem setters'

# A problem setter can create problems, edit the ones they are an author or curator of, upload their test data,
# and make their own problems public. They cannot edit other setters' problems or run contests.
PERMISSIONS = [
    'add_problem', 'change_problem', 'view_problem',
    'edit_own_problem', 'change_public_visibility', 'clone_problem',
    'add_problemgroup', 'view_problemgroup',
    'add_problemtype', 'view_problemtype',
    'view_language', 'view_license',
]


def add_group(apps, schema_editor):
    # Permissions are normally created after all migrations run; create them now so a fresh database works.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    group, _ = Group.objects.get_or_create(name=GROUP)
    group.permissions.add(*Permission.objects.filter(content_type__app_label='judge', codename__in=PERMISSIONS))


def remove_group(apps, schema_editor):
    apps.get_model('auth', 'Group').objects.filter(name=GROUP).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('judge', '0156_pnoi_points_from_difficulty'),
    ]

    operations = [
        migrations.RunPython(add_group, remove_group),
    ]
