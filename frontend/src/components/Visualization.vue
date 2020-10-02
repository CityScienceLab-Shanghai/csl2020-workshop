<template>
    <div class="visualization">
        <svg :width="width" :height="height"></svg>
        <canvas 
            :width="width * 2" :height="height * 2" 
            :style="{width: width + 'px', height: height + 'px'}"></canvas>
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
        step: Number,
        animate: Boolean,
    },
    data: function () {
        return {
            currentMode: 'home',
            currentTime: 0,
            dataset: {},
            customBase: document.createElement('custom'),
            width: window.innerWidth, 
            height: window.innerHeight,
            lastResize: 0,
        };
    },
    computed: {
        projection () {
            return d3.geoMercator()
                .center([-71.0865450, 42.3672538])
                .scale(1500000)
                .translate([this.width / 2, this.height / 2]);
        }
    },
    watch: {
        step () {
            this.dataset = this.simData[this.step];
            this.updateDataset();
        },

        simData () {
            this.dataset = this.simData[this.step];
            this.updateDataset();
        },

        currentMode () {
            console.log(this.currentMode);
        }
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

        drawMap() {
            return new Promise((resolve) => {
                var path = d3.geoPath().projection(this.projection);
                var gridUrl = "/geodata/grid80.geojson";
                var mapUrl = "/geodata/greater_area.geojson";
                
                Promise.all([d3.json(gridUrl), d3.json(mapUrl)]).then((results) => {
                    var grid = results[0];
                    var map = results[1];

                    var svg = d3.select(".visualization svg");
                    svg.selectAll("*").remove();

                    svg.append("path")
                        .attr("d", path(map))
                        .attr("fill", "white")
                        .attr("stroke", "lightgray");
                    
                    svg.append("path")
                        .attr("d", path(grid))
                        .attr("fill", "rgba(0, 0, 0, 0)")
                        .attr("stroke", "red");

                    resolve();
                });
            })
        },

        bindAgents() {
            var vis = d3.select(this.customBase);
            vis.selectAll("custom.circle")
                .data(this.dataset)
                .enter()
                .append("custom")
                .attr("class", 'circle')
                .attr("r", (d) => {
                    return d.population * 0.7 + 1.5;
                })
                .attr("x", (d) => {
                    return this.projection(d._coord)[0];
                })
                .attr("y", (d) => {
                    return this.projection(d._coord)[1];
                })
                .attr("fillStyle", (d) => {
                    return d.income === 0 ? 'rgba(255, 0, 0, 0.6)': 'rgba(0, 0, 255, 0.6)';
                })
        },

        drawAgents() {
            var vis = d3.select(this.customBase);
            var canvas = d3.select(".visualization canvas");
            var width = canvas.node().width;
            var height = canvas.node().height;
            var context = canvas.node().getContext('2d');

            context.save();

            context.scale(2, 2);
            context.clearRect(0, 0, this.width * 2, this.height * 2);
            var elements = vis.selectAll('custom.circle');

            function outOfBounds(x, y) {
                return x < 0 || x >= width || y < 0 || y >= height;
            }

            function drawAgent() {
                var node = d3.select(this);
                if (outOfBounds(node.attr('x'), node.attr('y'))) return;
                context.beginPath();
                context.arc(node.attr('x'), node.attr('y'), node.attr('r'), 0, 2 * Math.PI, false);
                context.fillStyle = node.attr('fillStyle');
                context.fill();
            }

            elements.each(drawAgent);

            context.restore();
        },

        updateAgents () {
            var vis = d3.select(this.customBase);
            vis.selectAll("custom.circle")
                .data(this.dataset)
                .transition()
                .delay(() => {
                    return gaussianRand() * 5000;
                })
                .duration(3000)
                .attr("r", (d) => {
                    return d.population * 0.7 + 1.5;
                })
                .attr("x", (d) => {
                    return this.projection(d._coord)[0];
                })
                .attr("y", (d) => {
                    return this.projection(d._coord)[1];
                })
                .attr("fillStyle", (d) => {
                    return d.income === 0 ? 'rgba(255, 0, 0, 0.6)': 'rgba(0, 0, 255, 0.6)';
                })

            var t = d3.timer((elapsed) => {
                this.drawAgents();
                if (elapsed > 8000) t.stop();
            }, 70);

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
    mounted () {
        function debounce(func){
            var timer;
            return function(event){
                if(timer) clearTimeout(timer);
                timer = setTimeout(func,500,event);
            };
        }
        window.addEventListener('resize', debounce(() => {
            console.log('debounce resize');
            this.width = window.innerWidth;
            this.height = window.innerHeight;
            
            this.drawMap().then(() => {
                this.updateDataset();
                var vis = d3.select(this.customBase);
                vis.selectAll("custom.circle")
                    .interrupt()
                    .data(this.dataset)
                    .attr("x", (d) => {
                        return this.projection(d._coord)[0];
                    })
                    .attr("y", (d) => {
                        return this.projection(d._coord)[1];
                    })
                this.drawAgents();
            });
        }));

        d3.json('agents_step0.json').then((data) => {
            this.$emit('agents-update', this.parseAgentStep(data));
        })
        
        this.drawMap().then(() => {
            this.bindAgents();
            this.drawAgents();
        });

        setInterval(() => {
            if (this.animate) {
                this.currentTime = (this.currentTime + 1) % (24 * 60);
                this.$emit('time-update', this.currentTime);
                if (this.currentTime === 7 * 60 || this.currentTime === 16 * 60) {
                    this.currentMode = this.currentMode === 'home' ? 'work' : 'home';
                    this.updateDataset();
                    this.updateAgents();
                }
            }
        }, 33);
    }
}
</script>

<style scoped>
.visualization {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    z-index: -1;
}

.visualization svg {
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: -1;
}

.visualization canvas {
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: 10;
}

.agent {
    position: absolute;
    transform: translate(-50%, -50%);
    background: rgba(255, 0, 0, 0.5);
    border-radius: 100%;

    transition: top 5s ease-in-out, left 5s ease-in-out;
}
</style>
