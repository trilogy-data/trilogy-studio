

<template>
    <v-dialog v-model="dialog" max-width="500" min-width=400>
        <template v-slot:activator="{ props }">
            <v-btn class="tab-btn pa-0 ba-0" v-bind="props" density="compact" icon="mdi-plus"
                v-shortkey.once="['ctrl', 'n']" @shortkey="showPopup()">
                +
            </v-btn>
        </template>
        <v-card theme="dark" class="mx-auto" min-width="344" title="Add Editor to Model">
            <v-form v-model="form" @submit.prevent="submit">
                <v-container>
                    <v-text-field variant="solo" density="compact" :readonly="loading" :rules="[required]" v-model="name"
                        label="Import as">
                    </v-text-field>
                    <v-divider />
                    <v-select variant="solo" density="compact" :readonly="loading" v-model="editor" label="Editor"
                        :items="editors" item-title="name">
                    </v-select>
                </v-container>
                <v-divider></v-divider>
                <v-alert class="mx-auto square-corners" color="warning" v-if="error">{{ error }}</v-alert>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :disabled="!form" :loading="loading" color="success" type="submit">
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
import { Model, LocalModel } from '/src/models/Model';
export default {
    name: "AddEditorToModelPopup",
    data() {
        return {
            form: false,
            loading: false,
            error: '',
            dialog: false,
            // model: null,
            name: '',
            extraValues: {},
        };
    },
    props: {
        model: [Model, LocalModel],
    },
    computed: {
        ...mapGetters(['editors']),
    },
    mounted: () => {
        // console.log(this.connections)
    },
    methods: {
        ...mapActions(['addEditorToModel']),
        showPopup() {
            this.dialog = true;
        },
        submit() {
            this.localAddConnection();
        },
        localAddEditorToModel() {
            this.addEditorToModel({
                name: this.name,
                type: this.selectedType,
                // model: this.model,
                extra: this.extraValues,
            }).then(() => {
                this.dialog = false;
                this.error = false;
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