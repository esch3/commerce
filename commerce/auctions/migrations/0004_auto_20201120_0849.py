# Generated by Django 3.1.3 on 2020-11-20 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionslisting',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='auctionslisting',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='auctionslisting',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='auctionslisting',
            name='user_id',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]