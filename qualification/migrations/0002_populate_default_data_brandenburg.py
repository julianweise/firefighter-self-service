# Generated by Django 3.1.2 on 2020-10-30 13:26

from django.db import migrations


class Migration(migrations.Migration):

    def populate_course(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        Course = apps.get_model('qualification', 'Course')
        tm1 = Course.objects.using(db_alias).create(name="Truppmann 1", abbreviation="TM1", sorting_order="1",
                                                    administration_level="ci", show_in_overview=True)
        funk = Course.objects.using(db_alias).create(name="Sprechfunker", abbreviation="Funk", sorting_order="2",
                                                     administration_level="co", show_in_overview=True)
        funk.requirements.set([tm1])
        agt = Course.objects.using(db_alias).create(name="Atemschutzgeräteträger", abbreviation="AGT",
                                                    sorting_order="3", administration_level="co", show_in_overview=True)
        agt.requirements.set([tm1, funk])
        tm2 = Course.objects.using(db_alias).create(name="Truppmann 2", abbreviation="TM2", sorting_order="4",
                                                    administration_level="ci", show_in_overview=True)
        tm2.requirements.set([tm1, funk])
        th = Course.objects.using(db_alias).create(name="Technische Hilfeleistung", abbreviation="TH",
                                                   sorting_order="5", administration_level="co", show_in_overview=True)
        th.requirements.set([tm1, tm2])
        ma = Course.objects.using(db_alias).create(name="Maschinisten", abbreviation="MA",
                                                   sorting_order="6", administration_level="co", show_in_overview=True)
        ma.requirements.set([tm1, tm2, funk])
        abc_ei = Course.objects.using(db_alias).create(name="ABC-Einsatz", abbreviation="ABCEi",
                                                       sorting_order="7", administration_level="co", show_in_overview=True)
        abc_ei.requirements.set([tm1, tm2, agt])
        abc_er = Course.objects.using(db_alias).create(name="ABC-Erkundung", abbreviation="ABCEr",
                                                       sorting_order="8", administration_level="co")
        abc_er.requirements.set([abc_ei])
        abc_de = Course.objects.using(db_alias).create(name="ABC-Dekon P/G", abbreviation="ABCDe",
                                                       sorting_order="9", administration_level="co",
                                                       show_in_overview=True)
        abc_de.requirements.set([abc_ei])
        tf = Course.objects.using(db_alias).create(name="Truppführer", abbreviation="TF", sorting_order="10",
                                                   administration_level="co", show_in_overview=True)
        tf.requirements.set([tm1, tm2, funk])
        gwt = Course.objects.using(db_alias).create(name="Gerätewart", abbreviation="GWT",
                                                    sorting_order="11", administration_level="st")
        gwt.requirements.set([tf, ma])
        gwt_pa = Course.objects.using(db_alias).create(name="Atemschutzgerätewart", abbreviation="GWTPA",
                                                       sorting_order="12", administration_level="st")
        gwt_pa.requirements.set([tf, agt])

        gf = Course.objects.using(db_alias).create(name="Gruppenführer", abbreviation="FIII",
                                                   sorting_order="13", administration_level="st", show_in_overview=True)
        gf.requirements.set([tf, funk])
        zf = Course.objects.using(db_alias).create(name="Zugführer", abbreviation="FIV",
                                                   sorting_order="14", administration_level="st")
        zf.requirements.set([gf])
        l_e_fw = Course.objects.using(db_alias).create(name="Leiter einer Freiwilligen Feuerwehr", abbreviation="FV",
                                                       sorting_order="15", administration_level="st",
                                                       show_in_overview=True)
        l_e_fw.requirements.set([zf])
        vf = Course.objects.using(db_alias).create(name="Verbandsführer", abbreviation="FVI",
                                                   sorting_order="16", administration_level="st")
        vf.requirements.set([zf])
        esa = Course.objects.using(db_alias).create(name="Einführung in die Stabsarbeit", abbreviation="ESA",
                                                    sorting_order="17", administration_level="st")
        esa.requirements.set([vf])
        f_abc = Course.objects.using(db_alias).create(name="Führen im ABC-Einsatz", abbreviation="FABC",
                                                      sorting_order="18", administration_level="st")
        f_abc.requirements.set([gf, abc_ei])
        owf = Course.objects.using(db_alias).create(name="Ortswehrführer", abbreviation="OWF",
                                                    sorting_order="19", administration_level="st")
        owf.requirements.set([gf])
        ab = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr", abbreviation="AB",
                                                   sorting_order="20", administration_level="st")
        ab.requirements.set([gf])
        ab_funk = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr Funk", abbreviation="ABF",
                                                        sorting_order="21", administration_level="st")
        ab_funk.requirements.set([ab, gf, funk])
        ab_ma = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr Machinist", abbreviation="ABMa",
                                                      sorting_order="22", administration_level="st")
        ab_ma.requirements.set([gf, ma])
        ab_agt = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr Atemschutzgeräteträger",
                                                       abbreviation="ABAGT", sorting_order="23",
                                                       administration_level="st")
        ab_agt.requirements.set([gf, agt])
        ab_abc = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr ABC",
                                                       abbreviation="ABAGT", sorting_order="24",
                                                       administration_level="st")
        ab_abc.requirements.set([ab, gf, f_abc])
        ab_th = Course.objects.using(db_alias).create(name="Ausbilder in der Feuerwehr Technische Hilfeleistung",
                                                       abbreviation="ABTH", sorting_order="25",
                                                       administration_level="st")
        ab_th.requirements.set([gf, th])
        juca1 = Course.objects.using(db_alias).create(name="Jugendleitercard (JuLeiCa) Teil 1",
                                                      abbreviation="juca1", sorting_order="26",
                                                      administration_level="st")
        juca2 = Course.objects.using(db_alias).create(name="Jugendleitercard (JuLeiCa) Teil 2",
                                                      abbreviation="juca2", sorting_order="27",
                                                      administration_level="st")

    def populate_legally_required_recurring_training(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        Training = apps.get_model('qualification', 'LegallyRequiredRecurringTraining')
        Course = apps.get_model('qualification', 'Course')
        tm1 = Course.objects.get(abbreviation="TM1")
        ma = Course.objects.get(abbreviation="MA")
        agt = Course.objects.get(abbreviation="AGT")
        abc_ei = Course.objects.get(abbreviation="ABCEi")
        uvv = Training.objects.using(db_alias).create(pk=0, name="Jährliche UVV-Unterweisung", recurring_interval='an',
                                                      training_course=tm1)
        stvo = Training.objects.using(db_alias).create(pk=1, name="Jährliche StVO-Unterweisung",
                                                       recurring_interval='an', training_course=ma)
        agt_t = Training.objects.using(db_alias).create(pk=2, name="Jährliche Atemschutzunterweisung",
                                                      recurring_interval='an', training_course=agt)
        agt_p = Training.objects.using(db_alias).create(pk=3, name="Jährliche PA-Belastungsübung",
                                                      recurring_interval='365', training_course=agt)
        abc_t = Training.objects.using(db_alias).create(pk=4, name="Jährliche ABC-Ausbildung", recurring_interval='an',
                                                        training_course=abc_ei)
        abc_p = Training.objects.using(db_alias).create(pk=5, name="Jährliche CSA-Belastungsübung",
                                                        recurring_interval='an', training_course=abc_ei)

    def populate_qualification_requirement(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        QualificationRequirement = apps.get_model('qualification', 'QualificationRequirement')
        Course = apps.get_model('qualification', 'Course')
        FitnessLevel = apps.get_model('fitness', 'FitnessLevel')
        Training = apps.get_model('qualification', 'LegallyRequiredRecurringTraining')

        agt = Course.objects.get(abbreviation="AGT")
        tm1 = Course.objects.get(abbreviation="TM1")
        ma = Course.objects.get(abbreviation="MA")
        abc_ei = Course.objects.get(abbreviation="ABCEi")
        g26_3 = FitnessLevel.objects.get(name="G26.3")
        pa_t = Training.objects.get(pk=2)
        pa_p = Training.objects.get(pk=3)
        uvv = Training.objects.get(pk=0)
        stvo = Training.objects.get(pk=1)
        abc_t = Training.objects.get(pk=4)
        abc_p = Training.objects.get(pk=5)

        QualificationRequirement.objects.using(db_alias).create(course=agt, fitness_level=g26_3,
                                                                required_training=pa_t)
        QualificationRequirement.objects.using(db_alias).create(course=agt, fitness_level=g26_3,
                                                                required_training=pa_p)
        QualificationRequirement.objects.using(db_alias).create(course=tm1, required_training=uvv)
        QualificationRequirement.objects.using(db_alias).create(course=ma, required_training=stvo)
        QualificationRequirement.objects.using(db_alias).create(course=abc_ei, fitness_level=g26_3,
                                                                required_training=abc_t)
        QualificationRequirement.objects.using(db_alias).create(course=abc_ei, fitness_level=g26_3,
                                                                required_training=abc_p)
    dependencies = [
        ('qualification', '0001_initial'),
        ('fitness', '0002_populate_default_data'),
    ]

    operations = [
        migrations.RunPython(populate_course),
        migrations.RunPython(populate_legally_required_recurring_training),
        migrations.RunPython(populate_qualification_requirement),
    ]
