# Generated by Django 2.1.1 on 2018-11-19 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configq', '0003_uploadquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_number',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='uploadquestion',
            name='image',
            field=models.ImageField(upload_to='questions/'),
        ),
    ]
