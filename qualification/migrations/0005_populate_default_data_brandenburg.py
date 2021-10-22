
from django.db import migrations


class Migration(migrations.Migration):

    def populate_course(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        Course = apps.get_model('qualification', 'Course')
        CourseRequirement = apps.get_model('qualification', 'CourseRequirement')
        mks_a = Course.objects.using(db_alias).create(name="Kettensägenausbildung A", abbreviation="MKSA",
                                                      sorting_order="29", administration_level="ci",
                                                      show_in_overview=True)
        mks_a_requirements = CourseRequirement.objects.using(db_alias).create()
        mks_a.requirements.set([mks_a_requirements])

        mks_b = Course.objects.using(db_alias).create(name="Kettensägenausbildung A", abbreviation="MKSA",
                                                      sorting_order="29", administration_level="ci",
                                                      show_in_overview=True)
        mks_b_requirements = CourseRequirement.objects.using(db_alias).create()
        mks_b_requirements.qualification_requirement.set([mks_a])
        mks_b.requirements.set([mks_b_requirements])


    dependencies = [
        ('qualification', '0003_populate_default_data_brandenburg'),
    ]

    operations = [
        migrations.RunPython(populate_course)
    ]
