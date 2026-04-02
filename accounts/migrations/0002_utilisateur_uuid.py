from django.db import migrations, models
import uuid


def generer_uuids(apps, schema_editor):
    Utilisateur = apps.get_model('accounts', 'Utilisateur')
    for user in Utilisateur.objects.all():
        user.uuid = uuid.uuid4()
        user.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids),
        migrations.AlterField(
            model_name='utilisateur',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]