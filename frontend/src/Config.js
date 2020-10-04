var tinycolor = require("tinycolor2");

function getThemeColor(color, opacity) {
    var colorString = getComputedStyle(document.body).getPropertyValue('--' + color);
    var colorData = tinycolor(colorString).setAlpha(opacity);
    return colorData.toRgbString();
}

export default {
    simulateApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/start",
    statusApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/status",
    resultsApi: "http://ec2-18-163-189-148.ap-east-1.compute.amazonaws.com:5000/debug_result",
    incentiveModes: ['No incentives', 'Static incentives', 'Dynamic incentives'],
    nonePanels: [
        {
            name: "No incentives",
            description: "This is a baseline simulation with no incentive policies.",
            controls: [], charts: []
        }
    ],
    staticPanels: [
        {
            name: "Static incentives",
            description: "Manually set incentives for the neighborhood.",
            controls: [
                {
                    id: "construction_intensity",
                    name: "Construction intensity",
                    min: 0, max: 1, default: 1, disabled: false
                },
                {
                    id: "rent_discount_ratio_all",
                    name: "Overall rent discount",
                    min: 0.1, max: 1, default: 1, disabled: false
                },
                {
                    id: "rent_discount_ratio_low_inc",
                    name: "Low income",
                    min: 0.1, max: 1, default: 1, disabled: false
                },
                {
                    id: "rent_discount_ratio_less_commuting",
                    name: "Less commuting",
                    min: 0.1, max: 1, default: 1, disabled: false
                },
                {
                    id: "rent_discount_ratio_small_scale",
                    name: "Small-scale housing",
                    min: 0.1, max: 1, default: 1, disabled: false
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
                    id: "diversity_target",
                    name: "Diversity",
                    min: 0.2, max: 0.7, default: 0.7, disabled: false
                },
                {
                    id: "low_inc_pop_ratio_target",
                    name: "Affordability",
                    min: 0.1, max: 0.7, default: 0.5, disabled: false
                },
                {
                    id: "commute_distance_target",
                    name: "Commute energy consumption",
                    min: 1.0, max: 3.5, default: 2, disabled: false
                },
                {
                    id: "building_energy_target",
                    name: "Building energy consumption",
                    min: 40, max: 80, default: 40, disabled: false
                }
            ],
            charts: []
        },
        {
            name: "Calculated incentives",
            description: "Incentives as calculated by the optimization algorithm.",
            controls: [
                {
                    id: "construction_intensity",
                    name: "Construction intensity",
                    min: 0, max: 1, default: 1, disabled: true
                },
                {
                    id: "rent_discount_ratio_all",
                    name: "Overall rent discount",
                    min: 0.1, max: 1, default: 1, disabled: true
                },
                {
                    id: "rent_discount_ratio_low_inc",
                    name: "Low income",
                    min: 0.1, max: 1, default: 1, disabled: true
                },
                {
                    id: "rent_discount_ratio_less_commuting",
                    name: "Less commuting",
                    min: 0.1, max: 1, default: 1, disabled: true
                },
                {
                    id: "rent_discount_ratio_small_scale",
                    name: "Small-scale housing",
                    min: 0.1, max: 1, default: 1, disabled: true
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
                                label: 'Current', 
                                data: [0, 0, 0, 0],
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1,
                                backgroundColor: getThemeColor('blue', 0.5)
                            },
                            { 
                                label: 'Baseline', 
                                data: [43.4297, 68.4488, 56.570344, 132.653],
                                borderColor: '#979797', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                }
            ],
        },
        {
            name: "Detailed information",
            description: "Here you can find the change of various indicators as time goes by, including developer finance, commute distance, population, and energy consumption.",
            controls: [],
            charts: [
                {
                    id: "developer-finance",
                    title: "Developer finance",
                    type: "line",
                    data: {
                        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                        datasets: [
                            { 
                                label: 'Finance', 
                                key: 'the_developer.finance',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Expenditure', 
                                key: 'the_developer.expenditure_total',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#D7A207', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Revenue', 
                                key: 'the_developer.revene_total',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#7ED321', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                },
                {
                    id: "commute-distance",
                    title: "Decrease in commute distance",
                    type: "line",
                    data: {
                        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                        datasets: [
                            { 
                                label: 'Mean distance', 
                                key: 'commute_distance_decrease',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                },
                {
                    id: "population",
                    title: "Population",
                    type: "line",
                    data: {
                        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                        datasets: [
                            { 
                                label: 'All', 
                                key: 'kendall_virtual_block.crt_total_pop',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Low income', 
                                key: 'kendall_virtual_block.crt_low_inc_pop',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#1CA9BF', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'High income', 
                                key: 'kendall_virtual_block.crt_high_inc_pop',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#D06DB2', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                },
                {
                    id: "energy",
                    title: "Residence energy consumption",
                    type: "line",
                    data: {
                        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                        datasets: [
                            { 
                                label: 'Residence energy', 
                                key: 'residence_energy_per_person',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                }
            ],
        },
    ]
}