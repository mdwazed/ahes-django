# Generated by Django 2.1.1 on 2019-03-28 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configq', '0014_exam_total_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionAns',
            field=models.TextField(max_length=500),
        ),
    ]