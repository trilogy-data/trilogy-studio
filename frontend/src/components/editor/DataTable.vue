

<template>
    <v-data-table density="compact" :headers="tableHeaders" :items="results" items-per-page="5">
        <template v-slot:item="{ item }">
            <tr :key="item.columns._index">
                <v-hover v-for="header in filteredHeaders" :key="header" v-slot="{ isHovering, props }">
                    <td class="text-truncate" style="max-width: 100px; min-width: 50px; position: relative;" :key="header"
                        v-bind="props">
                        <div v-if="isHovering" class="align-self-center" style="position: absolute;  top: 0;
      right: 0;">
                            <v-btn :color="transparent" :class="{ 'show-btns': isHovering }"
                                @click="copyText(item.columns[header])" icon="mdi-content-copy" size="x-small" ripple>
                            </v-btn>
                        </div>
                        {{ item.columns[header] }}

                        <v-tooltip v-if="item.columns[header] && item.columns[header].length > 25"
                            style="max-width: 400px; min-width: 200px;" activator="parent" :open-on-click="true"
                            location="bottom" close-delay="1000" open-delay="10000" content-class="custom-tooltip">{{
                                item.columns[header] }}</v-tooltip>

                    </td>
                </v-hover>
            </tr>
        </template>
    </v-data-table>
    <v-snackbar v-model="snackbar" timeout=2000>
        Copied text to clipboard
        <template v-slot:action="{ attrs }">
            <v-btn text v-bind="attrs" @click="snackbar = false"> Dismiss </v-btn>
        </template>
    </v-snackbar>
</template>
<style >
.custom-tooltip {
    opacity: 1 !important;

}

.show-btns {
    color: rgba(255, 255, 255, 1) !important;
}

.v-tooltip__content {
    font-size: 50px !important;
    opacity: 1 !important;
    display: block !important;
}
</style>
  
<script>
export default {
    props: {
        'headers': {
            type: Array,
            required: true,
        },
        'results': {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            snackbar: false,
            transparent: 'rgba(255, 255, 255, 0)',
        }
    },
    computed: {
        tableHeaders() {
            return this.filteredHeaders.map(x => ({ title: x, key: x }));
        },
        filteredHeaders() {
            return this.headers.filter(x => x !== '_index');
        }
    },
    methods: {
        async copyText(mytext) {
            try {
                await navigator.clipboard.writeText(mytext);
                this.snackbar = true
            } catch ($e) {
                alert('Cannot copy');
            }
        }
    },
}
</script>
  