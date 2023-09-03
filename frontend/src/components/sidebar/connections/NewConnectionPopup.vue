

<template>
    <v-dialog v-model="dialog" max-width="500" min-width=400>
        <template v-slot:activator="{ props }">
            <v-btn class="tab-btn pa-0 ba-0 " v-bind="props" density="compact" block>
                Add Connection
            </v-btn>
        </template>
        <v-card theme="dark" class="mx-auto" min-width="344" title="Add Connection">
            <v-form v-model="form">
                <v-container>
                    <v-form v-model="form">
                        <v-text-field variant="solo" density="compact" :readonly="loading" :rules="[required]"
                            v-model="name" label="Name">
                        </v-text-field>
                        <v-divider />
                        <v-select variant="solo" density="compact" :readonly="loading" :rules="[required]"
                            v-model="selectedType" label="Type" :items="connectionTypes">
                        </v-select>
                        <v-divider />
                        <v-select variant="solo" density="compact" :readonly="loading" v-model="model" label="Model"
                            :items="models" item-title="name">
                        </v-select>
                        <v-text-field v-for="field in extra" variant="solo" density="compact" :readonly="loading"
                            v-model="extraValues[field]" :label="field">
                        </v-text-field>

                    </v-form>
                </v-container>
                <v-divider></v-divider>
                <v-alert class="mx-auto square-corners" color="warning" v-if="error">{{ error }}</v-alert>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :disabled="!form" :loading="loading" color="success" @click="localAddConnection">
                        Add
                        <v-icon icon="mdi-chevron-right" end></v-icon>
                    </v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
    </v-dialog>
</template>
<style scoped>
.square-corners {
    border-radius: 0 !important;
}

.tab-btn {
    height: 25px;
    text-transform: none;
    color: var(--text-lighter);
    background-color: var(--main-bg-color);
    border-radius: 0;
}
</style>
<script lang="ts">
import { mapActions, mapGetters } from 'vuex';
import {getConnectionExtras } from './utility';
export default {
    name: "AddConnection",
    data() {
        return {
            form: false,
            loading: false,
            error: '',
            dialog: false,
            model: null,
            name: '',
            selectedType: 'duck_db',
            connectionTypes: ['duck_db', 'bigquery', 'sql_server'],
            extraValues: {},
        };
    },
    props: {
    },
    computed: {
        ...mapGetters(['models', 'getModelByName']),
        extra() {
            return getConnectionExtras(this.selectedType)
        },
    },
    mounted: () => {
        // console.log(this.connections)
    },
    methods: {
        ...mapActions(['addConnection']),
        showPopup() {
            this.dialog = true;
        },
        localAddConnection() {
            console.log(this.extraValues)
            this.addConnection({
                name: this.name,
                type: this.selectedType,
                model: this.model,
                extra: this.extraValues,
            }).then(() => {
                this.dialog = false;
                this.name = '';
            }).catch((e) => {
                this.error = e.message;
            });
        },
        required(v) {
            return !!v || 'Field is required'
        },
    },
};
</script>