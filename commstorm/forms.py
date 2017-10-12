# forms.py is IMPORTED INTO views.py
from django import forms
#weight forms
class RunWeightForm(forms.Form):
	runoff_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput1(this.value);'}),
		min_value=0.0,max_value=1.0)

class SedWeightForm(forms.Form):
	sedimentation_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput2(this.value);'}),
		min_value=0.0,max_value=1.0)

class AmenWeightForm(forms.Form):
	amenity_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput4(this.value);'}),
		min_value=0.0,max_value=1.0)
class AeWeightForm(forms.Form):
	aesthetic_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput3(this.value);'}),
		min_value=0.0,max_value=1.0)
class JobWeightForm(forms.Form):
	green_jobs_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput6(this.value);'}),
		min_value=0.0,max_value=1.0)

class CanWeightForm(forms.Form):
	green_canopy_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput5(this.value);'}),
		min_value=0.0,max_value=1.0)
class MaiWeightForm(forms.Form):
	maintenance_cost_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput7(this.value);'}),
		min_value=0.0,max_value=1.0)
class FeeWeightForm(forms.Form):
	fee_savings_weight = forms.FloatField(required=False, label = '', 
		widget=forms.NumberInput(attrs={'type':'range', 'step': '0.1',
			'onchange':'updateTextInput8(this.value);'}),
		min_value=0.0,max_value=1.0)
#benefit forms

class RunoffForm(forms.Form):
	runoff = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=20.5, initial=0.0)
class SedForm(forms.Form):
	sedimentation = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=998.18, initial=0.0)
class AeForm(forms.Form):
	aesthetics = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=560.0, initial=0.0)
class AmenForm(forms.Form):
	amenities = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=534.00, initial=0.0)
class CanForm(forms.Form):
	green_canopy = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=237.04, initial=0.0)
class JobForm(forms.Form):
	green_jobs = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=116.67, initial=0.0)
class MaiForm(forms.Form):
	maintenance_costs = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		max_value=226.71, initial=0.0)
class FeeForm(forms.Form):
	fee_saving = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=53.96, initial=0.0)

class BudgetForm(forms.Form):
	budget = forms.FloatField(required=False, label = '', widget = forms.NumberInput, 
		min_value=0.0, max_value=100000000.0, initial=0.0)


class fForm(forms.Form):
	res_frac = forms.FloatField(required=False, label = 'Residential', widget=forms.NumberInput,
		initial=0.0)
	com_frac = forms.FloatField(required=False, label = 'Commercial/Civic', widget=forms.NumberInput,
		initial=0.0)
	ind_frac = forms.FloatField(required=False, label = 'Industrial', widget=forms.NumberInput,
		initial=0.0)
	tran_frac = forms.FloatField(required=False, label = 'Transportation', widget=forms.NumberInput,
		initial=0.0)
	rec_frac = forms.FloatField(required=False, label = 'Recreation', widget=forms.NumberInput,
		initial=0.0)
	vac_frac = forms.FloatField(required=False, label = 'Vacant', widget=forms.NumberInput,
		initial=0.0)

class giForm(forms.Form):
	OPTIONS=(
		("gard","Rain Garden"),
		("tree","Tree Trench"),
		("perm","Porous Pavement"),
		("bar","Rain Barrel")
		)
	GI = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS,label='')
