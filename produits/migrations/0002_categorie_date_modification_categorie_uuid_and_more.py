from django.db import migrations, models
import uuid


def generer_uuids_categories(apps, schema_editor):
    Categorie = apps.get_model('produits', 'Categorie')
    for obj in Categorie.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


def generer_uuids_produits(apps, schema_editor):
    Produit = apps.get_model('produits', 'Produit')
    for obj in Produit.objects.all():
        obj.uuid = uuid.uuid4()
        obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='date_modification',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='categorie',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_categories),
        migrations.AlterField(
            model_name='categorie',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(generer_uuids_produits),
        migrations.AlterField(
            model_name='produit',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='unite',
            field=models.CharField(default='kg', max_length=20),
        ),
    ]