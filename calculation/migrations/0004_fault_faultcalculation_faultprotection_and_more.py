# Generated by Django 4.2.16 on 2024-11-29 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_protectiondevice_options_and_more"),
        (
            "calculation",
            "0003_faultcalculationprotocol_sensitivityanalysisprotocol_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Fault",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fault_type",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Вид КЗ"
                    ),
                ),
                (
                    "fault_type_designation",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Обозначение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вид КЗ",
                "verbose_name_plural": "Виды КЗ",
            },
        ),
        migrations.CreateModel(
            name="FaultCalculation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fault_location",
                    models.CharField(max_length=255, verbose_name="Узел КЗ"),
                ),
                (
                    "network_topology",
                    models.CharField(max_length=255, verbose_name="Схема сети"),
                ),
                ("fault_values", models.JSONField()),
                (
                    "fault_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fault_calculations",
                        to="calculation.fault",
                    ),
                ),
                (
                    "protection_half_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fault_calculations",
                        to="core.protectionhalfset",
                    ),
                ),
            ],
            options={
                "verbose_name": "Расчет токов КЗ",
                "verbose_name_plural": "Протоколы расчетов токов КЗ",
            },
        ),
        migrations.CreateModel(
            name="FaultProtection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.component"
                    ),
                ),
                (
                    "fault",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calculation.fault",
                    ),
                ),
            ],
            options={
                "verbose_name": "Назначение органов ДФЗ",
                "verbose_name_plural": "Назначение органов ДФЗ",
            },
        ),
        migrations.CreateModel(
            name="SensitivityAnalysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sensitivity_rate",
                    models.FloatField(verbose_name="Коэффициент чувствительности"),
                ),
                (
                    "fault_calculation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sensitivity_analysis",
                        to="calculation.faultcalculation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Анализ чувствительности",
                "verbose_name_plural": "Анализ чувствительности",
            },
        ),
        migrations.CreateModel(
            name="SettingsCalculation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("result_value", models.FloatField(verbose_name="Результат расчета")),
            ],
            options={
                "verbose_name": "Протокол расчета",
                "verbose_name_plural": "Протоколы расчетов",
            },
        ),
        migrations.RemoveField(
            model_name="sensitivityanalysisprotocol",
            name="fault_calculation_protocol",
        ),
        migrations.RemoveField(
            model_name="sensitivityanalysisprotocol",
            name="settings_calculation_protocol",
        ),
        migrations.RemoveField(
            model_name="settingscalculationprotocol",
            name="calculation_meta",
        ),
        migrations.RemoveField(
            model_name="settingscalculationprotocol",
            name="component",
        ),
        migrations.RemoveField(
            model_name="settingscalculationprotocol",
            name="protection_half_set",
        ),
        migrations.RenameField(
            model_name="calculationmeta",
            old_name="timestamp",
            new_name="calculation_date",
        ),
        migrations.AddField(
            model_name="calculationmeta",
            name="line",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="calculations",
                to="core.line",
            ),
        ),
        migrations.DeleteModel(
            name="FaultCalculationProtocol",
        ),
        migrations.DeleteModel(
            name="SensitivityAnalysisProtocol",
        ),
        migrations.DeleteModel(
            name="SettingsCalculationProtocol",
        ),
        migrations.AddField(
            model_name="settingscalculation",
            name="calculation_meta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="settings_calculations",
                to="calculation.calculationmeta",
            ),
        ),
        migrations.AddField(
            model_name="settingscalculation",
            name="component",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="settings_calculations",
                to="core.component",
            ),
        ),
        migrations.AddField(
            model_name="settingscalculation",
            name="protection_half_set",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="settings_calculations",
                to="core.protectionhalfset",
            ),
        ),
        migrations.AddField(
            model_name="sensitivityanalysis",
            name="settings_calculation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sensitivity_analysis",
                to="calculation.settingscalculation",
            ),
        ),
    ]
