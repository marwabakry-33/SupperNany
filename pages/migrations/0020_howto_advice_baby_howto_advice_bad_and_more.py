# Generated by Django 5.2 on 2025-05-20 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_howto_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='howto',
            name='advice_baby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.advicebaby'),
        ),
        migrations.AddField(
            model_name='howto',
            name='advice_bad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.advicebad'),
        ),
        migrations.AddField(
            model_name='howto',
            name='advice_bottle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.advicebottel'),
        ),
        migrations.AddField(
            model_name='howto',
            name='advice_moon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.advicemoon'),
        ),
        migrations.AddField(
            model_name='howto',
            name='advice_mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.advicemother'),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_af',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ar',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ar_dz',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ast',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_az',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_be',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_bg',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_bn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_br',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_bs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ca',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ckb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_cs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_cy',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_da',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_dsb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_el',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_en_au',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_en_gb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_eo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es_ar',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es_co',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es_mx',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es_ni',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_es_ve',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_et',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_eu',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_fa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_fi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_fr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_fy',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ga',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_gd',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_gl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_he',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_hi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_hr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_hsb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_hu',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_hy',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ig',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ind',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_io',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_is',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_it',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ja',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ka',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_kab',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_kk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_km',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_kn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ko',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ky',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_lb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_lt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_lv',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_mk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ml',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_mn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_mr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_my',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_nb',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ne',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_nl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_nn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_os',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_pa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_pl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_pt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_pt_br',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ro',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sq',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sr_latn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sv',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_sw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_te',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_tg',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_th',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_tk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_tr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_tt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_udm',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ug',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_uk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_ur',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_uz',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_vi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_zh_hans',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='content_zh_hant',
            field=models.TextField(blank=True, null=True),
        ),
    ]
