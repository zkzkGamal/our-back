# Generated by Django 5.0.2 on 2024-03-11 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_doctor_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='drugs_data',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.drugcategory'),
        ),
    ]
