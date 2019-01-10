# Generated by Django 2.1.1 on 2018-12-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0003_auto_20181209_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentans',
            name='auto_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='studentans',
            name='final_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='studentans',
            name='matching_confidence',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='studentans',
            name='students_ans',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]