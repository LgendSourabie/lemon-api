# Generated by Django 5.1.4 on 2024-12-20 22:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lemon_menuitems', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField(db_index=True)),
                ('delivery_crew', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_crew', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('menuitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemon_menuitems.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemon_orders.order')),
            ],
            options={
                'unique_together': {('menuitem', 'order')},
            },
        ),
    ]