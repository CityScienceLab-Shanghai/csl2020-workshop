<template>
    <div class="visualization">
        <!-- <img src="geodata/map.svg" /> -->
        <!-- <div class="agent" 
            v-for="agent in simData[step]" 
            :key="agent.name"
            :style="{
                top: transformAgent(agent[currentMode][0]) + 'px', 
                left: transformAgent(agent[currentMode][1]) + 'px',
                width: agent.population + 3 + 'px', 
                height: agent.population + 3 + 'px',
            }"></div>  -->
        <svg></svg>
    </div>
</template>

<script>
import * as d3 from 'd3';

function gaussianRand() {
  var rand = 0;
  for (var i = 0; i < 6; i += 1) {
    rand += Math.random();
  }
  return rand / 6;
}

export default {
    name: 'Visualization',
    props: {
        simData: Object,
        step: Number
    },
    data: function () {
        return {
            currentMode: 'home',
            dataset: {}
        };
    },
    methods: {
        parseAgentStep(data) {
            var parsedData = {};
            for (var step = 0; step < 12; step++) {
                if (!data[step]) continue;
                parsedData[step] = [];
                for (var agentid in data[step].name) {
                    parsedData[step].push( {
                        name: data[step].name[agentid],
                        home: data[step].home_loc[agentid],
                        work: data[step].work_loc[agentid],
                        population: data[step].population[agentid], 
                        income: data[step].income[agentid]
                    } );
                }
            }
            return parsedData;
        },

        draw() {
            var svg = d3.select(".visualization svg");
            var projection = d3.geoMercator()
                //.center([-71.0682, 42.3602])
                .center([-71.0933, 42.3737])
                .scale(1500000)
                //.translate([window.innerWidth / 2, window.innerHeight / 2]);
                //.clipExtent([[-71.0933, 42.3737], [-71.3933, 42.6737]])
            var path = d3.geoPath().projection(projection);

            var gridUrl = "/geodata/grid80.geojson";
            var mapUrl = "/geodata/greater_area.geojson";
            
            Promise.all([d3.json(gridUrl), d3.json(mapUrl)]).then((results) => {
                var grid = results[0];
                var map = results[1];

                svg.append("path")
                    .attr("d", path(map))
                    .attr("fill", "white")
                    .attr("stroke", "lightgray");
                
                svg.append("path")
                    .attr("d", path(grid))
                    .attr("fill", "rgba(0, 0, 0, 0)")
                    .attr("stroke", "red");

                
                console.log("drawing", this.dataset);

                svg.selectAll("circle")
                    .data(this.dataset)
                    .enter()
                    .append("circle")
                    .attr("r", (d) => {
                        return d.population * 0.7 + 1.5;
                    })
                    .attr("cx", (d) => {
                        return projection(d._coord)[0];
                    })
                    .attr("cy", (d) => {
                        return projection(d._coord)[1];
                    })
                    .attr("fill", (d) => {
                        return d.income === 0 ? 'red': 'blue';
                    })
                    .attr("opacity", 0.6)
            });
        },

        update () {
            var svg = d3.select(".visualization svg");
            var projection = d3.geoMercator()
                //.center([-71.0682, 42.3602])
                .center([-71.0933, 42.3737])
                .scale(1500000)
            
            svg.selectAll("circle")
                .data(this.dataset)
                .transition()
                .delay(() => {
                    return gaussianRand() * 3500;
                })
                .duration(3000)
                .attr("r", (d) => {
                    return d.population * 0.7 + 1.5;
                })
                .attr("cx", (d) => {
                    return projection(d._coord)[0];
                })
                .attr("cy", (d) => {
                    return projection(d._coord)[1];
                })
                .attr("fill", (d) => {
                    return d.income === 0 ? 'red': 'blue';
                })
        },

        updateDataset() {
            for (var i in this.dataset) {
                this.dataset[i]._coord = this.dataset[i][this.currentMode];
            }
        },

        transformAgent(coord) {
            return (coord - 8000) / 4 - 400;
        }
    },
    watch: {
        simData () {
            this.dataset = this.simData[this.step];
            this.updateDataset();
        },

        currentMode () {
            console.log(this.currentMode);
        }
    },
    mounted () {
        d3.json('agents_step0.json').then((data) => {
            this.$emit('agents-update', this.parseAgentStep(data));
        })

        this.draw();

        setInterval(() => {
            this.currentMode = this.currentMode === 'home' ? 'work' : 'home';
            this.updateDataset();
            this.update();
        }, 10000);
    }
}
</script>

<style scoped>
.visualization {
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
}

.visualization svg {
    width: 100%;
    height: 100%;
}

.agent {
    position: absolute;
    transform: translate(-50%, -50%);
    background: rgba(255, 0, 0, 0.5);
    border-radius: 100%;

    transition: top 5s ease-in-out, left 5s ease-in-out;
}
</style>
