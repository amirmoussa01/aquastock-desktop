from django.db import migrations, models
import uuid


def generer_uuids_mouvements(apps, schema_editor):
    MouvementStock = apps.get_model('stock', 'MouvementStock')
    for obj in MouvementStock.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mouvementstock',
            name='synced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mouvementstock',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_mouvements),
        migrations.AlterField(
            model_name='mouvementstock',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]