# Generated by Django 3.1.3 on 2020-11-25 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20201125_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('WPN', 'Weapons'), ('GRN', 'Greens'), ('TEC', 'Technology'), ('AFT', 'Artifact'), ('OTR', 'Other')], max_length=3),
        ),
    ]
