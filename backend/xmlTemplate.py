import string

keys = ['normalized_rent_discount_ratio_low_inc', 'normalized_rent_discount_ratio_less_commuting', 'normalized_rent_discount_ratio_small_scale', 
'normalized_diversity_target', 'normalized_low_inc_pop_ratio_target', 'normalized_commute_distance_decrease_target', 'normalized_building_energy_target', 
'incentive_policy', 'dynamic_policy']

defaultValue = {key:'0' if key not in ['incentive_policy', 'dynamic_policy'] else 'True' for key in keys}
defaultValue['id'] = '1'

t = string.Template("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Experiment_plan>
	<Simulation id="${id}" sourcePath="/home/ubuntu/csl2020-workshop/backend/backend-gama/models/workshop.gaml" finalStep="13" experiment="gui">
	  <Parameters>
		<Parameter name="normalized_rent_discount_ratio_low_inc" type="FLOAT" value="${normalized_rent_discount_ratio_low_inc}" />
		<Parameter name="normalized_rent_discount_ratio_less_commuting" type="FLOAT" value="${normalized_rent_discount_ratio_less_commuting}" />
		<Parameter name="normalized_rent_discount_ratio_small_scale" type="FLOAT" value="${normalized_rent_discount_ratio_small_scale}" />
		<Parameter name="normalized_diversity_target" type="FLOAT" value="${normalized_diversity_target}" />
		<Parameter name="normalized_low_inc_pop_ratio_target" type="FLOAT" value="${normalized_low_inc_pop_ratio_target}" />
		<Parameter name="normalized_commute_distance_decrease_target" type="FLOAT" value="${normalized_commute_distance_decrease_target}" />
		<Parameter name="normalized_building_energy_target" type="FLOAT" value="${normalized_building_energy_target}" />
		<Parameter name="incentive_policy" type="BOOLEAN" value="${incentive_policy}" />
		<Parameter name="dynamic_policy" type="BOOLEAN" value="${dynamic_policy}" />
	  </Parameters>
	  <Outputs>
		<Output id="1" name="normalized_mean_commute_distance_decrease" framerate="1" />
		<Output id="2" name="normalized_kendall_diversity" framerate="1" />
		<Output id="3" name="normalized_kendall_low_inc_ratio" framerate="1" />
		<Output id="4" name="normalized_residence_energy_per_person" framerate="1" />
		<Output id="5" name="the_developer.finance" framerate="1" />
		<Output id="6" name="the_developer.expenditure_total" framerate="1" />
		<Output id="7" name="the_developer.revene_total" framerate="1" />
		<Output id="8" name="commute_distance_decrease" framerate="1" />
		<Output id="9" name="kendall_virtual_block.crt_total_pop" framerate="1" />
		<Output id="10" name="kendall_virtual_block.crt_low_inc_pop" framerate="1" />
		<Output id="11" name="kendall_virtual_block.crt_high_inc_pop" framerate="1" />
		<Output id="12" name="residence_energy_per_person" framerate="1" />
		<Output id="13" name="Name List" framerate="1" />
		<Output id="14" name="Work Loc List" framerate="1" />
		<Output id="15" name="Home Loc List" framerate="1" />
		<Output id="16" name="Population List" framerate="1" />
		<Output id="17" name="Income List" framerate="1" />
		<Output id="18" name="grids_with_top6_potential" framerate="1" />
	  </Outputs>
	</Simulation>
</Experiment_plan>""")

def getXML(**newValue):
    tempValue = defaultValue.copy()
    for k, v in newValue.items():
        if k in tempValue.keys():
            tempValue[k] = v
    return t.safe_substitute(tempValue)

# if __name__ == "__main__":
#     print(t.safe_substitute(values))
