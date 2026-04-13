# Generated migration for LoginLog model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('success', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
    ]
