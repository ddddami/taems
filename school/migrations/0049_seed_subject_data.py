# Generated by Django 4.1.7 on 2023-06-24 06:24
from django.db import migrations


def create_subject_groups(apps, schema_editor):
    SubjectGroup = apps.get_model('school', 'SubjectGroup')
    subject_groups_data = [
        'Core',
        'Optional',
        'Trade',
        'Science',
        'Commercial',
        'Hummanities',
    ]
    subject_groups = [SubjectGroup(title=title)
                      for title in subject_groups_data]
    SubjectGroup.objects.bulk_create(subject_groups)


def create_subjects(apps, schema_editor):
    SubjectGroup = apps.get_model('school', 'SubjectGroup')
    Subject = apps.get_model('school', 'Subject')
    # Another implementation, not sure which is better
    # subject_list = ['English Language', 'Mathematics', 'Civic Education',
    #                 'Further Mathematics', 'Computer Science',
    #                 'Animal Husbandry', 'Marketing', 'Data Processing',
    #                 'Technical Drawing', 'Further Mathematics', 'Agricultural Science',
    #                 'Geography', 'Economics', 'Physics', 'Biology', 'Chemistry',
    #                 'Commerce', 'Accounting', 'Economics', 'Government', 'Yoruba/Igbo', 'Food & Nutrition', 'CRS/IRK',
    #                 'Literature in English', 'Literature', 'Biology', 'CRS/IRK',
    #                 'Government', 'Food & Nutrition', 'Nigerian Languages']
    # subjects = [Subject(name=name) for name in subject_list]
    # Subject.objects.bulk_create(subjects)

    # core = SubjectGroup.objects.get(name='Core')
    # science = SubjectGroup.objects.get(name='Science')
    # commercial = SubjectGroup.objects.get(name='Commercial')
    # hummanities = SubjectGroup.objects.get(name='Hummanities')
    # trade = SubjectGroup.objects.get(name='Trade')
    subject_data = {
        'CORE': ['English Language', 'Mathematics', 'Civic Education'],
        'OPTIONAL': ['Further Mathematics', 'Computer Science'],
        'TRADE': ['Animal Husbandry', 'Marketing', 'Data Processing'],
        'SCIENCE': ['Technical Drawing', 'Further Mathematics', 'Agricultural Science',
                    'Geography', 'Economics', 'Physics', 'Biology', 'Chemistry'],
        'COMMERCIAL': ['Commerce', 'Accounting', 'Economics', 'Government', 'Yoruba/Igbo', 'Food & Nutrition', 'CRS/IRK'],
        'HUMMANITIES': ['Literature in English', 'Literature', 'Biology', 'CRS/IRK',
                        'Government', 'Food & Nutrition', 'Nigerian Languages'],
    }
    for group_name, subjects in subject_data.items():
        subject_group = SubjectGroup.objects.get(title=group_name)
        for subject_name in subjects:
            subject, created = Subject.objects.get_or_create(
                title=subject_name)
            subject_group.subjects.add(subject)


def delete_subject_groups(apps, schema_editor):
    SubjectGroup = apps.get_model('school', 'SubjectGroup')
    SubjectGroup.objects.all().delete()


def delete_subjects(apps, schema_editor):
    Subject = apps.get_model('school', 'Subject')
    Subject.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0048_remove_subject_group_subject_groups'),
    ]

    operations = [
        migrations.RunPython(create_subject_groups, delete_subject_groups),
        migrations.RunPython(create_subjects, delete_subjects),
    ]
