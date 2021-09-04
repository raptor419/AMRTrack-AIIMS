# -*- encoding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader, exceptions
from django.http import HttpResponse
from app.forms import *
from app.scripts.viewmethods import *
from app.scripts.bokeh import *
from app.variables import *
from authentication.models import *
from app.models import *
from datetime import datetime

from bokeh.embed import components
# import pandas as pd


@login_required(login_url="/login/")
def index(request):
    site_count = len(Patient.objects.values('department').distinct())
    user_count = User.objects.count()
    test_count = PathTest.objects.count()
    patient_count = len(Patient.objects.values('patient_id').distinct())
    # print(test_count, patient_count, site_count, user_count)
    count = {"site": site_count, "test": test_count, "patient": patient_count, "user": user_count}
    pie, site_df = pie_path()
    table = site_df.to_html(classes="table fixed", index=False)
    script, div = components(pie)
    # print(table)
    return render(request, "index.html", {'table': div, 'script': script,
                                          'count': count, "sitetable": table})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))
    except exceptions.TemplateDoesNotExist:
        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def antibiogram(request):
    msg = None
    table = None
    success = False
    if request.method == "POST":
        input_form = InputDataForm(data=request.POST)
        if input_form.is_valid():

            if not input_form.cleaned_data['ams']:
                input_form.cleaned_data['ams'] = ANTIMICROBIALS
            if not input_form.cleaned_data['site']:
                input_form.cleaned_data['site'] = SITES
            if not input_form.cleaned_data['col']:
                input_form.cleaned_data['col'] = COLLTYPES
            if not input_form.cleaned_data['org']:
                input_form.cleaned_data['org'] = ORGANISMS
            if not input_form.cleaned_data['hosp']:
                input_form.cleaned_data['hosp'] = HOSPTIALS
            if not input_form.cleaned_data['startdate']:
                input_form.cleaned_data['startdate'] = datetime(2010, 1, 1).date()
            if not input_form.cleaned_data['enddate']:
                input_form.cleaned_data['enddate'] = datetime(2050, 1, 1).date()

            # print(input_form.cleaned_data)

            dfr, dfs, dfi = get_rsi(ams=input_form.cleaned_data['ams'],
                                    organisms=input_form.cleaned_data['org'],
                                    colltypes=input_form.cleaned_data['col'],
                                    sites=input_form.cleaned_data['site'],
                                    hosp=input_form.cleaned_data['hosp'],
                                    startdate=input_form.cleaned_data['startdate'],
                                    enddate=input_form.cleaned_data['enddate'])

            hosp = input_form.cleaned_data['hosp']


            dft = dfi + dfr + dfs
            dff = dfs / (dft) * 100

            

            #remove all organism if only one organism is selected
            if len(input_form.cleaned_data['org'])==1:
                dff = dff.drop(' All Organisms')
                dft = dft.drop(' All Organisms')
                
            #set precision
            dff = dff.round(decimals=1)

            #remove antimicrobal with all NaN value
            dff = dff.dropna(axis=1, how='all', inplace=False)
            dft = dft.replace(0, np.nan)
            dft = dft.dropna(axis=1, how='all', inplace=False)

            hmap = heatmap(dff, dft, s_z="Sensitivity")
            script1, div1 = components(hmap)

            return render(request, 'pages/antibiogram.html',
                          {'table': div1, 'script': script1, "hospitals": hosp})

        else:
            msg = 'Form is not valid'

    else:
        input_form = InputDataForm()

    return render(request, "pages/antibiogramform.html",
                  {"form": input_form, "table": table, "msg": msg, "success": success})


def ml_analysis(request):
    if request.method == 'POST':
        input_form = InputForm2(data=request.POST)
        input_form.fields['ams2'].choices = [(x, x) for x in ANTIMICROBIALS]
        # print(input_form)
        if input_form.is_valid():
            if not input_form.cleaned_data['ams2']:
                input_form.cleaned_data['ams2'] = ANTIMICROBIALS[0]
            ams = input_form.cleaned_data['ams2']
            # print(ams)
            input_form = InputForm2()
            input_form.fields['ams2'].choices = [(x, x) for x in ANTIMICROBIALS]
            return render(request, 'pages/ml_view.html', {'form': input_form, 'pic': ams})
        else:
            print(input_form.errors)
    else:
        input_form = InputForm2()

    return render(request, 'pages/ml_view.html', {'form': input_form})
