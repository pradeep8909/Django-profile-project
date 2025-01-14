# Generated by Django 5.0.6 on 2024-08-05 04:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.PositiveIntegerField(choices=[(0, 'Inactive'), (2, 'Active'), (1, 'Migrated'), (3, 'Archived')], default=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='SEO friendly url, use only aplhabets and hyphen')),
                ('front_link', models.CharField(blank=True, max_length=512)),
                ('backend_link', models.CharField(blank=True, max_length=512)),
                ('icon', models.CharField(blank=True, max_length=512)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='userprofile.menus')),
            ],
            options={
                'verbose_name_plural': 'Menus',
                'ordering': ('order',),
            },
        ),
    ]
