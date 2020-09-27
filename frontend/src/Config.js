var tinycolor = require("tinycolor2");

function getThemeColor(color, opacity) {
    var colorString = getComputedStyle(document.body).getPropertyValue('--' + color);
    var colorData = tinycolor(colorString).setAlpha(opacity);
    return colorData.toRgbString();
}

export default {
    simulateApi: "",
    statusApi: "",
    resultsApi: "",
    controlPanels: [
        {
            name: "Low-income residents",
            description: "Describes the preferences of low-income residents, like moving, commute distance, and house prices.",
            controls: [
                {
                    id: "b_move_low_inc",
                    name: "Moving",
                    default: -1.43
                },
                {
                    id: "b_commute_distance_low_inc",
                    name: "Commute distance",
                    default: -0.88
                },
                {
                    id: "b_large_size_low_inc",
                    name: "Large size",
                    default: 0.24
                },
                {
                    id: "b_price_low_low_inc",
                    name: "Low price",
                    default: -0.002
                },
                {
                    id: "b_pop_density_low_inc",
                    name: "Low population density",
                    default: -0.0056
                },
                {
                    id: "b_inc_disparity_low_inc",
                    name: "Low income disparity",
                    default: -0.21
                },
            ],
            charts: []
        },
        {
            name: "High-income residents",
            description: "Describes the preferences of high-income residents.",
            controls: [
                {
                    id: "b_move_high_inc",
                    name: "Moving",
                    default: -1.29
                },
                {
                    id: "b_commute_distance_high_inc",
                    name: "Commute distance",
                    default: -0.81
                },
                {
                    id: "b_large_size_high_inc",
                    name: "Large size",
                    default: 0.52
                },
                {
                    id: "b_price_low_high_inc",
                    name: "Low price",
                    default: -0.0006
                },
                {
                    id: "b_pop_density_high_inc",
                    name: "Low population density",
                    default: -0.0123
                },
                {
                    id: "b_inc_disparity_high_inc",
                    name: "Low income disparity",
                    default: -0.52
                },
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
                        labels: ['Density', 'Diversity', 'Equality', 'Environment'],
                        datasets: [
                            { 
                                label: 'Baseline', 
                                data: [15, 25, 10, 5],
                                borderColor: getThemeColor('gray', 0.5),
                                backgroundColor: getThemeColor('gray', 0.2) 
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
                                label: 'Density', 
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
                                label: 'Equality', 
                                data: [5, 15, 10, 15, 10, 10, 25, 20, 20, 25, 15, 5],
                                fill: false,
                                borderColor: getThemeColor('green', 0.5)
                            },
                            { 
                                label: 'Environment', 
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