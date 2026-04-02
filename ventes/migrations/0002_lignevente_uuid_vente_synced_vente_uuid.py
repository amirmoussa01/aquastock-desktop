from django.db import migrations, models
import uuid


def generer_uuids_ventes(apps, schema_editor):
    Vente = apps.get_model('ventes', 'Vente')
    for obj in Vente.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


def generer_uuids_lignes(apps, schema_editor):
    LigneVente = apps.get_model('ventes', 'LigneVente')
    for obj in LigneVente.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vente',
            name='synced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vente',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_ventes),
        migrations.AlterField(
            model_name='vente',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='lignevente',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_lignes),
        migrations.AlterField(
            model_name='lignevente',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
