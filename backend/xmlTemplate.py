import string

keys = ['diversity_target', 'low_inc_pop_ratio_target', 'commute_distance_target', 
'building_energy_target', 'construction_intensity', 'rent_discount_ratio_all', 'rent_discount_ratio_low_inc', 
'rent_discount_ratio_less_commuting', 'rent_discount_ratio_small_scale', 'incentive_policy', 'dynamic_policy']

defaultValue = {key:'0' for key in keys}
defaultValue['id'] = '1'

t = string.Template("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Experiment_plan>
	<Simulation id="${id}" sourcePath="/home/ubuntu/Model/models/workshop.gaml" finalStep="13" experiment="gui">
	  <Parameters>
	  	<Parameter name="construction_intensity" type="FLOAT" value="${construction_intensity}" />
		<Parameter name="rent_discount_ratio_all" type="FLOAT" value="${rent_discount_ratio_all}" />
		<Parameter name="rent_discount_ratio_low_inc" type="FLOAT" value="${rent_discount_ratio_low_inc}" />
		<Parameter name="rent_discount_ratio_less_commuting" type="FLOAT" value="${rent_discount_ratio_less_commuting}" />
		<Parameter name="rent_discount_ratio_small_scale" type="FLOAT" value="${rent_discount_ratio_small_scale}" />
		<Parameter name="diversity_target" type="FLOAT" value="${diversity_target}" />
		<Parameter name="low_inc_pop_ratio_target" type="FLOAT" value="${low_inc_pop_ratio_target}" />
		<Parameter name="commute_distance_target" type="FLOAT" value="${commute_distance_target}" />
		<Parameter name="building_energy_target" type="FLOAT" value="${building_energy_target}" />
		<Parameter name="incentive_policy" type="BOOLEAN" value="${incentive_policy}" />
		<Parameter name="dynamic_policy" type="BOOLEAN" value="${dynamic_policy}" />
	  </Parameters>
	  <Outputs>
		<Output id="1" name="mean_commute_distance" framerate="1" />
		<Output id="2" name="kendall_diversity" framerate="1" />
		<Output id="3" name="kendall_low_inc_ratio" framerate="1" />
		<Output id="4" name="residence_energy_per_person" framerate="1" />
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
