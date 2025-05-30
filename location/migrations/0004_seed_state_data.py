# Generated by Django 4.1.7 on 2023-06-03 08:18

from django.db import migrations, transaction


def seed_data(apps, schema_editor):
    states_data = [
        {
            "id": 1,
            "name": "Anambra"
        },
        {
            "id": 2,
            "name": "Enugu"
        },
        {
            "id": 3,
            "name": "Akwa Ibom"
        },
        {
            "id": 4,
            "name": "Adamawa"
        },
        {
            "id": 5,
            "name": "Abia"
        },
        {
            "id": 6,
            "name": "Bauchi"
        },
        {
            "id": 7,
            "name": "Bayelsa"
        },
        {
            "id": 8,
            "name": "Benue"
        },
        {
            "id": 9,
            "name": "Borno"
        },
        {
            "id": 10,
            "name": "Cross River"
        },
        {
            "id": 11,
            "name": "Delta"
        },
        {
            "id": 12,
            "name": "Ebonyi"
        },
        {
            "id": 13,
            "name": "Edo"
        },
        {
            "id": 14,
            "name": "Ekiti"
        },
        {
            "id": 15,
            "name": "Gombe"
        },
        {
            "id": 16,
            "name": "Imo"
        },
        {
            "id": 17,
            "name": "Jigawa"
        },
        {
            "id": 18,
            "name": "Kaduna"
        },
        {
            "id": 19,
            "name": "Kano"
        },
        {
            "id": 20,
            "name": "Katsina"
        },
        {
            "id": 21,
            "name": "Kebbi"
        },
        {
            "id": 22,
            "name": "Kogi"
        },
        {
            "id": 23,
            "name": "Kwara"
        },
        {
            "id": 24,
            "name": "Lagos"
        },
        {
            "id": 25,
            "name": "Nasarawa"
        },
        {
            "id": 26,
            "name": "Niger"
        },
        {
            "id": 27,
            "name": "Ogun"
        },
        {
            "id": 28,
            "name": "Ondo"
        },
        {
            "id": 29,
            "name": "Osun"
        },
        {
            "id": 30,
            "name": "Oyo"
        },
        {
            "id": 31,
            "name": "Plateau"
        },
        {
            "id": 32,
            "name": "Rivers"
        },
        {
            "id": 33,
            "name": "Sokoto"
        },
        {
            "id": 34,
            "name": "Taraba"
        },
        {
            "id": 35,
            "name": "Yobe"
        },
        {
            "id": 36,
            "name": "Zamfara"
        },
        {
            "id": 37,
            "name": "F.C.T"
        }
    ]

    State = apps.get_model('location', 'State')

    states = [State(id=state['id'], name=state['name'])
              for state in states_data]

    State.objects.bulk_create(states)
    print('Done.')


def revert_data(apps, schema_editor):
    State = apps.get_model('location', 'State')
    State.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_remove_lga_code'),
    ]

    operations = [
        migrations.RunPython(seed_data, revert_data)
    ]
