import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0155_pnoi_organization_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='points',
            field=models.FloatField(
                help_text='Set automatically from the difficulty (difficulty divided by 100). '
                          'Only type points for a problem with no difficulty estimate.',
                validators=[django.core.validators.MinValueValidator(0)], verbose_name='points'),
        ),
    ]
