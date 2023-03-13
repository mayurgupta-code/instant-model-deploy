# Generated by Django 4.0 on 2023-03-13 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_mlmodelinput_input_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodelinput',
            name='input_type',
            field=models.CharField(choices=[('str', 'text'), ('checkbox', 'checkbox'), ('float', 'number'), ('file', 'file'), ('image', 'image')], default='float', max_length=100),
        ),
    ]