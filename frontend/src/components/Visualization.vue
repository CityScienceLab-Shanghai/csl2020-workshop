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
        highlights: {
            type: Array,
            default: () => {return []}
        },
        mapData: Array
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
            highIncomeColor: '#D06DB2',
            lowIncomeColor: '#1CA9BF'
        };
    },
    computed: {
        projection () {
            return d3.geoMercator()
                .center([-71.0865450, 42.3672538])
                .scale(1500000)
                .translate([this.width / 2 - this.width / 20, this.height / 2]);
        }
    },
    watch: {
        step () {
            this.currentTime = 0;
            if (!this.simData[this.step]) return;   // No data loaded yet.
            this.dataset = this.simData[this.step];
            this.updateDataset();
            this.bindAgents();
            this.drawAgents();
        },

        simData () {
            this.dataset = this.simData[this.step];
            this.updateDataset();
            this.bindAgents();
            this.drawAgents();
            this.currentTime = 0;
        },

        highlights () {
            d3.selectAll('polygon')
                .attr("fill", "#141414")
                .attr("stroke", "#303030")
                .attr("stroke-width", 1);

            for (var boxId of this.highlights) {
                d3.select('polygon#' + boxId)
                    .attr("fill", "#46730E")
                    .attr("stroke", "#89C743")
                    .attr("stroke-width", 2)
                    .each(function () { this.parentNode.appendChild(this); });
            }
        },

        mapData () {
            this.drawMap();
            this.bindAgents();
            this.drawAgents();
        }
    },
    methods: {

        drawMap() {
            if (this.mapData.length < 2) return;    // Haven't finished loading.

            var path = d3.geoPath().projection(this.projection);
            var grid = this.mapData[0];
            var map = this.mapData[1];

            grid = grid.name.map((name, index) => {
                return {
                    name: name,
                    coords: grid.shape[index].slice(1)
                }
            })

            var svg = d3.select(".visualization svg");
            svg.selectAll("*").remove();

            svg.append("path")
                .attr("d", path(map))
                .attr("fill", "rgb(0, 0, 0)")
                .attr("stroke", "#303030");
            
            svg.append("g")
                .attr('id', 'grid')
                .selectAll('polygon')
                .data(grid)
                .enter().append("polygon")
                .attr("points", (box) => { 
                    return box.coords.map((point) => {
                        return [this.projection(point)[0], this.projection(point)[1]].join(",");
                    }).join(" ");
                })
                .attr('id', box => box.name)
                .attr("fill", "#141414")
                .attr("stroke", "#303030")
                .attr("stroke-location", "inside");
        },

        bindAgents() {
            var vis = d3.select(this.customBase);
            vis.selectAll("*").remove();
            vis.selectAll("custom.circle")
                .data(this.dataset)
                .enter()
                .append("custom")
                .attr("class", 'circle')
                .attr("r", (d) => {
                    return Math.log(d.population * 1.5 + 2 + 1 / Math.E);
                })
                .attr("x", (d) => {
                    return this.projection(d._coord)[0];
                })
                .attr("y", (d) => {
                    return this.projection(d._coord)[1];
                })
                .attr("fillStyle", (d) => {
                    return d.income === 0 ? this.lowIncomeColor : this.highIncomeColor;
                })

                .exit().remove()
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
                    return gaussianRand() * 7000;
                })
                .duration(2000)
                .attr("r", (d) => {
                    return Math.log(d.population * 1.5 + 2 + 1 / Math.E);
                })
                .attr("x", (d) => {
                    return this.projection(d._coord)[0];
                })
                .attr("y", (d) => {
                    return this.projection(d._coord)[1];
                })
                .attr("fillStyle", (d) => {
                    return d.income === 0 ? this.lowIncomeColor: this.highIncomeColor;
                })

            var t = d3.timer((elapsed) => {
                this.drawAgents();
                if (elapsed > 10000) t.stop();
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
            
            this.drawMap();

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
        }));

        setInterval(() => {
            if (this.animate) {
                this.currentTime = (this.currentTime + 1) % (24 * 60);
                this.$emit('time-update', this.currentTime);
                if (this.currentTime === 6 * 60 + 30 || this.currentTime === 16 * 60) {
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
