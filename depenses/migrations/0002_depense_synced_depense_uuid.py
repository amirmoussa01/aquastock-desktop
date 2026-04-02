from django.db import migrations, models
import uuid


def generer_uuids_depenses(apps, schema_editor):
    Depense = apps.get_model('depenses', 'Depense')
    for obj in Depense.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='depense',
            name='synced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='depense',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_depenses),
        migrations.AlterField(
            model_name='depense',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]