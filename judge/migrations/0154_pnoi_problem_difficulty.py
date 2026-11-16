import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0153_pnoi_school_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='difficulty_estimate',
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name='difficulty estimate',
                help_text='Your own guess of the difficulty on the rating scale: 800 is the easiest, 1200 is a '
                          'typical beginner problem, 2000 and above is hard. Shown, marked as an estimate, until '
                          'the site can calculate the difficulty from a rated contest.',
                validators=[django.core.validators.MinValueValidator(800),
                            django.core.validators.MaxValueValidator(3500)]),
        ),
        migrations.AddField(
            model_name='problem',
            name='difficulty_calculated',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='calculated difficulty'),
        ),
        migrations.AddField(
            model_name='problem',
            name='difficulty',
            field=models.IntegerField(blank=True, db_index=True, editable=False, null=True,
                                      verbose_name='difficulty'),
        ),
    ]
