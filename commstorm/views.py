from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages 
from forms import *
from stormwise_grnacr_com import storm_2_djang,treat
from django.forms import formset_factory
from django.core.exceptions import ValidationError
import json


def overbrook(request):
	
	if request.method == 'GET':

		bud = BudgetForm(request.GET)
		run = RunoffForm(request.GET)
		wr = RunWeightForm(request.GET)
		wam = AmenWeightForm(request.GET)
		wae = AeWeightForm(request.GET)
		wc = CanWeightForm(request.GET)
		wj = JobWeightForm(request.GET)
		wm = MaiWeightForm(request.GET)
		wf = FeeWeightForm(request.GET)

		arrayb = []
		arrayz = []
		dictz = {}
		dictb = {}
		dictl = {}
		gi_set="default"
		fracs = "default"
		amenmax = 109.0
		aemax = 37.0

		if bud.is_valid():
			budanswer = bud.cleaned_data['budget']

		if run.is_valid():
			runanswer = run.cleaned_data['runoff']

		if wr.is_valid():
			w1 = wr.cleaned_data['runoff_weight']

		if wam.is_valid():
			w4 = wam.cleaned_data['amenity_weight']

		if wae.is_valid():
			w3 = wae.cleaned_data['aesthetic_weight']

		if wc.is_valid():
			w5 = wc.cleaned_data['green_canopy_weight']

		if wj.is_valid():
			w6 = wj.cleaned_data['green_jobs_weight']

		if wm.is_valid():
			w7 = wm.cleaned_data['maintenance_cost_weight']

		if wf.is_valid():
			w8 = wf.cleaned_data['fee_savings_weight']
		
				
		if runanswer != None:
			runoff = runanswer
		else:
			runoff = 0.0
		if w1 != None or w3 != None or w4 != None or w5 != None or w6 != None or w7 != None or w8 != None:		
			if w1 != None and w3 != None and w4 != None and w5 != None and w6 != None and w7 != None and w8 != None:	
				weights = {'1_volume':w1,'3_aesthetics':w3,'4_amenity':w4,'5_green_canopy':w5,'6_job':w6,'7_m_cost':w7,'8_fee_saving':w8}		
			else:
				messages.error(request, "Error: Please fill all fields")
			if budanswer != None:
				budget = budanswer
				budget = budget/1000.0
			else:
				messages.error(request, "Error: Please input budget or runoff goal")
				budget = 0.0
			yamldoc = 'overbrook.yaml'	
			storm = storm_2_djang(yamldoc,budget,runoff,weights,fracs,gi_set)
			goal = storm[0]
			check = storm[1]
			if check == "infeasible":
				messages.error(request,'Infeasible problem -> Reduce runoff or increase budget')
			b_amen = (goal['benTotsByBenefit']['4_amenity'])/amenmax * 100.0
			b_aesth = (goal['benTotsByBenefit']['3_aesthetics'])/aemax * 100.0
			b_maint = (goal['benTotsByBenefit']['7_m_cost'])*-1
			arrayb = [goal['benTotsByBenefit']['1_volume'],b_aesth,b_amen,goal['benTotsByBenefit']['5_green_canopy'],goal['benTotsByBenefit']['6_job'],b_maint,goal['benTotsByBenefit']['8_fee_saving']]
			#for i in len(goal['invTotsByGi'].values()):
			#	arrayz.append(goal['invTotsByGi'].values()[i])
			dictz = goal['invTotsByGi']
			dictb = goal['benTotsByBenefitByGi']
			dictl = goal['invTotsByLanduse']
			messages.info(request, '%.2f' % goal['investmentTotal'])
	else:
	
		run = RunoffForm()
		wr = RunWeightForm()
		wam = AmenWeightForm()
		wae = AeWeightForm()
		wc = CanWeightForm()
		wj = JobWeightForm()
		wm = MaiWeightForm()
		wf = FeeWeightForm()

		bud = BudgetForm()

	return render(request,'overbrook.html', 
		{'bud':bud,'run':run,'wr':wr, 'wam':wam, 'wae':wae,
			'wc':wc, 'wj':wj, 'wm':wm, 'wf':wf, 'arrayb':arrayb, 'dictb':json.dumps(dictb), 
			'dictz':json.dumps(dictz),'dictl':json.dumps(dictl)})	

def overbrook_advanced(request):
	fFormSet = formset_factory(fForm, extra=4)

	res_vals = []
	com_vals = []
	ind_vals = []
	tran_vals = []
	rec_vals = []
	vac_vals = []
	arrayb = []
	arrayz = []
	dictz = {}
	fracs = {'2_rain_garden':{},'3_tree_trench':{},'7_permeable_pavement':{},'8_cistern':{}}
	gi_set = []

	if request.method == 'POST':

		bud = BudgetForm(request.POST)
		run = RunoffForm(request.POST)
		wr = RunWeightForm(request.POST)
		wam = AmenWeightForm(request.POST)
		wae = AeWeightForm(request.POST)
		wc = CanWeightForm(request.POST)
		wj = JobWeightForm(request.POST)
		wm = MaiWeightForm(request.POST)
		wf = FeeWeightForm(request.POST)

		
		amenmax = 109.0
		aemax = 37.0

		if bud.is_valid():
			budanswer = bud.cleaned_data['budget']

		if run.is_valid():
			runanswer = run.cleaned_data['runoff']

		if wr.is_valid():
			w1 = wr.cleaned_data['runoff_weight']

		if wam.is_valid():
			w4 = wam.cleaned_data['amenity_weight']

		if wae.is_valid():
			w3 = wae.cleaned_data['aesthetic_weight']

		if wc.is_valid():
			w5 = wc.cleaned_data['green_canopy_weight']

		if wj.is_valid():
			w6 = wj.cleaned_data['green_jobs_weight']

		if wm.is_valid():
			w7 = wm.cleaned_data['maintenance_cost_weight']

		if wf.is_valid():
			w8 = wf.cleaned_data['fee_savings_weight']
		
				
		if runanswer != None:
			runoff = runanswer

		if w1 != None or w3 != None or w4 != None or w5 != None or w6 != None or w7 != None or w8 != None:		
			if w1 != None and w3 != None and w4 != None and w5 != None and w6 != None and w7 != None and w8 != None:	
				weights = {'1_volume':w1, '3_aesthetics':w3,'4_amenity':w4,'5_green_canopy':w5,'6_job':w6,'7_m_cost':w7,'8_fee_saving':w8}		
			else:
				messages.error(request, "Error: Please fill all fields")
			if budanswer != None:
				budget = budanswer
				budget = budget/1000.0
			else:
				messages.error(request, "Error: Please input budget")
			yamldoc = 'overbrook_reduced.yaml'	
			

		f_formset = fFormSet(request.POST, request.FILES)
		GIset = giForm(request.POST)
		if GIset.is_valid():
			gi_set = GIset.cleaned_data.get('GI')
		if f_formset.is_valid():
			for f_form in f_formset:
				res_frac = f_form.cleaned_data.get('res_frac')
				if res_frac == None:
					res_vals.append(0.0)
				else:
					res_vals.append(res_frac)	
				com_frac = f_form.cleaned_data.get('com_frac')
				if com_frac == None:
					com_vals.append(0.0)
				else:
					com_vals.append(com_frac)	
				ind_frac = f_form.cleaned_data.get('ind_frac')
				if ind_frac == None:
					ind_vals.append(0.0)
				else:
					ind_vals.append(ind_frac)	
				tran_frac = f_form.cleaned_data.get('tran_frac')
				if tran_frac == None:
					tran_vals.append(0.0)
				else:
					tran_vals.append(tran_frac)	
				rec_frac = f_form.cleaned_data.get('rec_frac')
				if rec_frac == None:
					rec_vals.append(0.0)
				else:
					rec_vals.append(rec_frac)	
				vac_frac = f_form.cleaned_data.get('vac_frac')
				if vac_frac == None:
					vac_vals.append(0.0)
				else:
					vac_vals.append(vac_frac)	

		fracs['2_rain_garden']['1_residential'] = res_vals[0]
		fracs['3_tree_trench']['1_residential'] = res_vals[1]
		fracs['7_permeable_pavement']['1_residential'] = res_vals[2]
		fracs['8_cistern']['1_residential'] = res_vals[3]

		fracs['2_rain_garden']['2_commercial'] = com_vals[0]
		fracs['3_tree_trench']['2_commercial'] = com_vals[1]
		fracs['7_permeable_pavement']['2_commercial'] = com_vals[2]
		fracs['8_cistern']['2_commercial'] = com_vals[3]

		fracs['2_rain_garden']['3_industrial'] = ind_vals[0]
		fracs['3_tree_trench']['3_industrial'] = ind_vals[1]
		fracs['7_permeable_pavement']['3_industrial'] = ind_vals[2]
		fracs['8_cistern']['3_industrial'] = ind_vals[3]

		fracs['2_rain_garden']['5_transportation'] = tran_vals[0]
		fracs['3_tree_trench']['5_transportation'] = tran_vals[1]
		fracs['7_permeable_pavement']['5_transportation'] = tran_vals[2]
		fracs['8_cistern']['5_transportation'] = tran_vals[3]

		fracs['2_rain_garden']['6_recreation'] = rec_vals[0]
		fracs['3_tree_trench']['6_recreation'] = rec_vals[1]
		fracs['7_permeable_pavement']['6_recreation'] = rec_vals[2]
		fracs['8_cistern']['6_recreation'] = rec_vals[3]

		fracs['2_rain_garden']['9_vacant'] = vac_vals[0]
		fracs['3_tree_trench']['9_vacant'] = vac_vals[1]
		fracs['7_permeable_pavement']['9_vacant'] = vac_vals[2]
		fracs['8_cistern']['9_vacant'] = vac_vals[3]

		yamldoc = 'overbrook_reduced.yaml'	
		storm = storm_2_djang(yamldoc,budget,runoff,weights,fracs,gi_set)
		goal = storm[0]
		check = storm[1]
		if check == "infeasible":
			messages.error(request,'Infeasible problem -> Reduce runoff or increase budget')
		b_amen = (goal['benTotsByBenefit']['4_amenity'])/amenmax * 100.0
		b_aesth = (goal['benTotsByBenefit']['3_aesthetics'])/aemax * 100.0
		b_maint = (goal['benTotsByBenefit']['7_m_cost'])*-1
		arrayb = [goal['benTotsByBenefit']['1_volume'],b_aesth,b_amen,goal['benTotsByBenefit']['5_green_canopy'],goal['benTotsByBenefit']['6_job'],b_maint,goal['benTotsByBenefit']['8_fee_saving']]
			
		dictz = goal['invTotsByGi']
		messages.info(request, '%.2f' % goal['investmentTotal'])
	else:
		f_formset = fFormSet()
		GIset = giForm()
		
		run = RunoffForm()
		wr = RunWeightForm()
		wam = AmenWeightForm()
		wae = AeWeightForm()
		wc = CanWeightForm()
		wj = JobWeightForm()
		wm = MaiWeightForm()
		wf = FeeWeightForm()

		bud = BudgetForm()
	return render(request,'advanced.html',{'f_formset':f_formset,'GIset':GIset,'bud':bud,'run':run,'wr':wr, 'wam':wam, 'wae':wae,
			'wc':wc, 'wj':wj, 'wm':wm, 'wf':wf, 'arrayb':arrayb, 
			'dictz':json.dumps(dictz)})


#def overbrook_advanced(request):
