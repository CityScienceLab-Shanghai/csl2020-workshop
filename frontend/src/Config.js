var tinycolor = require("tinycolor2");

function getThemeColor(color, opacity) {
    var colorString = getComputedStyle(document.body).getPropertyValue('--' + color);
    var colorData = tinycolor(colorString).setAlpha(opacity);
    return colorData.toRgbString();
}

export default {
    simulateApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/start",
    statusApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/status",
    resultsApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/result",
    incentiveModes: ['No incentives', 'Static incentives', 'Dynamic incentives'],
    staticPanels: [
        {
            name: "Static incentives",
            description: "Manually set incentives for the neighborhood.",
            controls: [
                {
                    id: "b_move_low_inc",
                    name: "Moving",
                    default: -1.43
                }
            ],
            charts: []
        },
    ],

    dynamicPanels: [
        {
            name: "Optimization goals",
            description: "Set goals for the equity and environmental impact of the neighborhood, and have the algorithm find optimized dynamic incentives.",
            controls: [
                {
                    id: "Low Income Proportion",
                    name: "Low income proportion",
                    default: 0.5
                },
                {
                    id: "Diversity",
                    name: "Diversity",
                    default: 0.5
                },
                {
                    id: "All",
                    name: "Commute energy consumption",
                    default: 0.5
                },
                {
                    id: "Building energy consumption",
                    name: "Building energy consumption",
                    default: 0.5
                }
            ],
            charts: []
        },
    ],

    outputPanels: [
        {
            name: "Overall assessment",
            description: "Assessment of the diversity, equality, and environment of the neighborhood.",
            controls: [],
            charts: [
                {
                    id: "overall",
                    type: "radar",
                    data: {
                        labels: ['Affordability', 'Diversity', ['Building', 'Energy', 'Consumption'], ['Commute', 'Energy', 'Consumption']],
                        datasets: [
                            { 
                                label: 'Baseline', 
                                data: [15, 25, 10, 5],
                                borderColor: getThemeColor('gray', 0.5),
                                backgroundColor: getThemeColor('gray', 0.2) 
                            },
                            { 
                                label: 'Goal', 
                                data: [100, 100, 100, 100],
                                borderColor: getThemeColor('green', 0.5),
                                backgroundColor: getThemeColor('green', 0)
                            },
                            { 
                                label: 'Current', 
                                data: [80, 15, 50, 30],
                                borderColor: getThemeColor('blue', 0.5),
                                backgroundColor: getThemeColor('blue', 0.2)
                            },
                        ]
                    }
                },
                {
                    id: "running-history",
                    type: "line",
                    data: {
                        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        datasets: [
                            { 
                                label: 'Affordability', 
                                data: [20, 25, 15, 5, 15, 30, 20, 10, 5, 15, 10, 15],
                                fill: false,
                                borderColor: getThemeColor('blue', 0.5)
                            },
                            { 
                                label: 'Diversity', 
                                data: [15, 30, 20, 10, 5, 15, 10, 15, 10, 10, 25, 20],
                                fill: false,
                                borderColor: getThemeColor('cyan', 0.5)
                            },
                            { 
                                label: 'Building Energy Consumption', 
                                data: [5, 15, 10, 15, 10, 10, 25, 20, 20, 25, 15, 5],
                                fill: false,
                                borderColor: getThemeColor('green', 0.5)
                            },
                            { 
                                label: 'Commute Energy Consumption', 
                                data: [10, 10, 25, 20, 20, 25, 15, 5, 5, 15, 10, 15],
                                fill: false,
                                borderColor: getThemeColor('yellow', 0.5)
                            }
                        ]
                    }

                }
            ],
        },
    ]
}