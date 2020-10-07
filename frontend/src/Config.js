var tinycolor = require("tinycolor2");

function getThemeColor(color, opacity) {
    var colorString = getComputedStyle(document.body).getPropertyValue('--' + color);
    var colorData = tinycolor(colorString).setAlpha(opacity);
    return colorData.toRgbString();
}

export default {
    // simulateApi: "http://workshop.citysciencelabshanghai.media/api/start",
    // statusApi: "http://workshop.citysciencelabshanghai.media/api/status",
    // resultsApi: "response.json",
    // stopApi: "http://workshop.citysciencelabshanghai.media/api/stop",

    simulateApi: "/api/start",
    statusApi: "/api/status",
    resultsApi: "/api/result",
    stopApi: "/api/stop",
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
            name: "Static incentive strength",
            description: "Manually set incentives for the neighborhood.",
            controls: [
                // {
                //     id: "construction_intensity",
                //     name: "Construction intensity",
                //     min: 0, max: 1, default: 1, disabled: false
                // },
                // {
                //     id: "rent_discount_ratio_all",
                //     name: "Overall rent discount",
                //     min: 0.1, max: 1, default: 1, disabled: false
                // },
                {
                    id: "normalized_rent_discount_ratio_low_inc",
                    name: "Low income",
                    min: 1, max: 0.5, default: 0, disabled: false
                },
                {
                    id: "normalized_rent_discount_ratio_less_commuting",
                    name: "Less commuting",
                    min: 1, max: 0.5, default: 0, disabled: false
                },
                {
                    id: "normalized_rent_discount_ratio_small_scale",
                    name: "Small-scale housing",
                    min: 1, max: 0.5, default: 0, disabled: false
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
                    id: "normalized_low_inc_pop_ratio_target",
                    name: "Affordability",
                    min: 0.35, max: 0.65, default: 0.5, disabled: false
                },
                {
                    id: "normalized_diversity_target",
                    name: "Diversity",
                    min: 0.62, max: 0.7, default: 0.5, disabled: false
                },
                {
                    id: "normalized_commute_distance_decrease_target",
                    name: "Commute energy efficiency",
                    min: 0, max: 0.6, default: 0.5, disabled: false
                },
                {
                    id: "normalized_building_energy_target",
                    name: "Building energy efficiency",
                    min: 60, max: 50, default: 0.5, disabled: false
                }
            ],
            charts: []
        },
    ],

    outputPanels: [
        {
            name: "Urban performance",
            description: "Assessment of the social and environmental urban performance of the community.",
            controls: [],
            charts: [
                {
                    id: "overall",
                    type: "radar",
                    data: {
                        labels: ['Affordability', 'Diversity', ['Building', 'Energy', 'Efficiency'], ['Commute', 'Energy', 'Efficiency']],
                        datasets: [
                            { 
                                label: 'Current', 
                                data: [0, 0, 0, 0],
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1,
                                backgroundColor: getThemeColor('blue', 0.5)
                            },
                            { 
                                label: 'Baseline', 
                                data: [56.7432, 92.30286, 63.56628, 11.51480],
                                borderColor: '#979797', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Last', 
                                data: [0, 0, 0, 0],
                                borderColor: 'rgba(66,143,253,1)', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Goal', 
                                data: [0, 0, 0, 0],
                                borderColor: 'rgba(126,211,33)', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                }
            ],
        },
        {
            name: "Detailed information",
            description: "Here you can find the change of various indicators as time goes by, such as developer finance, population, and energy consumption.",
            controls: [],
            charts: [
                {
                    id: "developer-finance",
                    title: "Developer finance",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
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
                                borderColor: 'rgba(215,162,7,0.5)', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Revenue', 
                                key: 'the_developer.revene_total',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: 'rgba(126,211,33,0.5)', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Danger Zone', 
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: 'start',
                                backgroundColor: "rgba(255, 0, 0, 0.2)",
                                borderColor: "rgba(255, 0, 0, 0.5)",
                                borderWidth: 1, pointRadius: 0
                            },
                        ]
                    }
                },
                {
                    id: "population",
                    title: "Population",
                    indicator: " (Affordability)",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
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
                    id: "diversity",
                    title: "Population Diversity",
                    indicator: " (Diversity)",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        datasets: [
                            { 
                                label: 'Diversity', 
                                key: 'normalized_kendall_diversity',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                },
                {
                    id: "commute-distance",
                    title: "Decrease in commute distance",
                    indicator: " (Commute energy efficiency)",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        datasets: [
                            { 
                                label: 'Decrease in distance', 
                                key: 'commute_distance_decrease',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Danger Zone', 
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: 'start',
                                backgroundColor: "rgba(255, 0, 0, 0.2)",
                                borderColor: "rgba(255, 0, 0, 0.5)",
                                borderWidth: 1, pointRadius: 0
                            }
                        ]
                    }
                },
                {
                    id: "energy",
                    title: "Residence energy consumption",
                    indicator: " (Building energy efficiency)",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
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
                },
                {
                    id: "policies",
                    title: "Incentive policies",
                    type: "line",
                    data: {
                        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        datasets: [
                            { 
                                label: 'Low income', 
                                key: 'normalized_rent_discount_ratio_low_inc',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#428FFD', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Less commuting', 
                                key: 'normalized_rent_discount_ratio_small_scale',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#d7a207', borderWidth: 2, pointRadius: 1
                            },
                            { 
                                label: 'Small-scale housing', 
                                key: 'normalized_rent_discount_ratio_less_commuting',
                                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                fill: false,
                                borderColor: '#7ed321', borderWidth: 2, pointRadius: 1
                            }
                        ]
                    }
                }
            ],
        },
    ]
}