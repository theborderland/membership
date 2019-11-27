# Generated by Django 2.2.7 on 2019-11-27 21:08

from django.db import migrations, models
import django.db.models.deletion
import pretix.base.models.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pretixbase', '0141_seat_sorting_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('voucher', models.PositiveIntegerField(null=True)),
                ('ip', models.CharField(max_length=200)),
                ('cookie', models.CharField(max_length=200)),
                ('browser', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.Event')),
            ],
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.AddConstraint(
            model_name='lotteryform',
            constraint=models.UniqueConstraint(fields=('event', 'email'), name='register_email_once'),
        ),
        migrations.AddConstraint(
            model_name='lotteryform',
            constraint=models.UniqueConstraint(fields=('event', 'first_name', 'last_name', 'dob'), name='register_person_once'),
        ),
    ]
