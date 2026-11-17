import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0154_pnoi_problem_difficulty'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='organization name')),
                ('about', models.TextField(verbose_name='what the organization is for')),
                ('is_open', models.BooleanField(default=True, verbose_name='anyone can join',
                                                help_text='If unticked, students have to ask to join.')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='request time')),
                ('state', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')],
                                           db_index=True, default='P', max_length=1, verbose_name='state')),
                ('reply', models.CharField(blank=True, default='', max_length=300, verbose_name='reply to the student',
                                           help_text='Optional. Shown to the student, for example why the request '
                                                     'was rejected.')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   related_name='+', to='judge.organization',
                                                   verbose_name='organization created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='organization_proposals', to='judge.profile',
                                           verbose_name='requested by')),
            ],
            options={
                'verbose_name': 'request to start an organization',
                'verbose_name_plural': 'requests to start an organization',
                'ordering': ['-time'],
            },
        ),
    ]
