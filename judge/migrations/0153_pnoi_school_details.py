from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0152_deactivate_user_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='school',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='school'),
        ),
        migrations.AddField(
            model_name='profile',
            name='grade_class_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='year of finishing Grade 12'),
        ),
        migrations.AddField(
            model_name='profile',
            name='student_status',
            field=models.CharField(blank=True, choices=[('college', 'College'), ('none', 'Not a student')],
                                   default='', max_length=10, verbose_name='student status'),
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='region'),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_school',
            field=models.BooleanField(default=True, verbose_name='show school details on profile'),
        ),
    ]
