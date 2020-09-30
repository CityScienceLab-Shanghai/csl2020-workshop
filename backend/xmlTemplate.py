import string

defaultValue = {'id': '1', 'b_move_low_inc':'0.0'}

t = string.Template("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Experiment_plan>
	<Simulation id="${id}" sourcePath="/home/ubuntu/Model/models/workshop.gaml" finalStep="13" experiment="gui">
	  <Parameters>
	  	<Parameter name="b_move_low_inc" type="FLOAT" value="${b_move_low_inc}" />
	  </Parameters>
	  <Outputs>
		<Output id="1" name="Move to Kendall: Low Income" framerate="1" />
		<Output id="2" name="Move to Kendall: High Income" framerate="1" />
		<Output id="3" name="Move out of Kendall: Low Income" framerate="1" />
		<Output id="4" name="Move out of Kendall: High Income" framerate="1" />
		<Output id="5" name="Occupancy" framerate="1" />
		<Output id="6" name="All" framerate="1" />
		<Output id="7" name="Work in Kendall" framerate="1" />
		<Output id="8" name="Live in Kendall" framerate="1" />
		<Output id="9" name="Work or Live in Kendall" framerate="1" />
		<Output id="10" name="Diversity" framerate="1" />
		<Output id="11" name="Low Income Proportion" framerate="1" />
	  </Outputs>
	</Simulation>
</Experiment_plan>""")

def getXML(**newValue):
    tempValue = defaultValue.copy()
    for k, v in newValue.items():
        if k in tempValue.keys():
            tempValue[k] = v
    return t.safe_substitute(tempValue)

if __name__ == "__main__":
    print(t.safe_substitute(values))
