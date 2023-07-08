

<template>
      <DataTable class="fill-width ma-0 ma-sm-2 px-0 px-sm-2" :headers="headers" :results="results" />
    <v-chip-group v-if="validChartTypes.length > 1" column v-model="mode" selected-class="text-deep-purple-accent-4"
        mandatory align-self="end" class="text-right">

        <v-chip v-for="option in validChartTypes" :key="option" :value="option" density="compact">{{ option }}</v-chip>
    </v-chip-group>
    <div v-if="mode === Display.TABLE">
        <DataTable class="fill-width ma-0 ma-sm-2 px-0 px-sm-2" :headers="headers" :results="results" />
    </div>
    <div v-else-if="mode === Display.BAR_CHART">
        <apexchart class="fill-width ma-0 ma-sm-2 px-0 px-sm-2" type="bar" :options="chartOptions" :series="series">
        </apexchart>
    </div>
    <div v-else-if="mode === Display.LINE_CHART">
        <apexchart class="fill-width ma-0 ma-sm-2 px-0 px-sm-2" type="line" :options="chartOptions" :series="series">
        </apexchart>
    </div>
</template>
<script>
import DataTable from '/src/components/query/DataTable.vue'
import charts from '/src/helpers/charts'
let Display = charts.Display()
const DisplayMap = new Map();

// Figure out how to not have to synchronize this with backend
DisplayMap.set(1, Display.TABLE);
DisplayMap.set(2, Display.BAR_CHART);
DisplayMap.set(3, Display.LINE_CHART);

export default {
    props: {
        'headers': {
            type: Array,
            required: true,
        },
        'results' : {
            type: Array,
            required: true,
        },
        'columns': {
            type: Object,
            required:true,
        },
        'defaultMode': {
            required: false,
            default: Display.TABLE
        },

    }, //['headers', 'results', 'columns', 'defaultMode'],
    components: {
        DataTable,
    },
    data() {

        var mode = Display.TABLE;
        if (this.defaultMode) {
            mode = DisplayMap.get(this.defaultMode);
        }
        return {
            mode: mode,
            Display

        }
    },

    computed: {
        /*eslint no-unused-vars: ["error", { "argsIgnorePattern": "^_" }]*/

        safe_columns() {
            if (this.columns) {
                return Object.entries(this.columns).map(([_k, v]) => v);
            }
            return []
        },
        tableHeaders() {
            return this.safe_columns.map(v => ({ title: v.name, key: v.name }));
        },

        validChartTypes() {
            return charts.validChartTypes(this.safe_columns);
        },
        chartOptions() {
            let dimension = ''
            let type = 'category';
            if (this.mode === charts.Display().BAR_CHART) {
                dimension = charts.getDimensions(this.safe_columns)[0];
            }
            else if (this.mode === charts.Display().LINE_CHART) {
                dimension = charts.getDateDimensions(this.safe_columns)[0];
                type = 'datetime';
            }
            else {
                return {}
            }
            let x_axis = this.results.map(y => y[dimension.name]);
            let output = {
                chart: {
                    id: 'query_display',
                    background: '#15141A',
                    animations: {
                        enabled: false,
                        // easing: 'easeinout',
                        // speed: 800,
                        // animateGradually: {
                        //     enabled: true,
                        //     delay: 150
                        // },
                        // dynamicAnimation: {
                        //     enabled: true,
                        //     speed: 350
                        // }
                    }
                },
                xaxis: {
                    type: type,
                    categories: x_axis,
                },
                yaxis: {
                    forceNiceScale: true,
                },
                theme: {
                    mode: 'dark',
                },

            };
            return output
        },
        series() {
            let metrics = charts.getMetrics(this.safe_columns);
            let values = metrics.map(x =>
            ({
                name: x.name,
                data: this.results.map(y => y[x.name]),
            })
            );
            return values
        }
    },

};
</script>