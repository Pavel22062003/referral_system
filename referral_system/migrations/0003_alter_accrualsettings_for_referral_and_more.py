# Generated by Django 5.0.4 on 2024-04-22 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0002_accrualsettings_rename_customer_referral_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accrualsettings',
            name='for_referral',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='accrualsettings',
            name='for_referral_code_owner',
            field=models.IntegerField(default=20),
        ),
    ]
