

<template>
    <v-dialog v-model="dialog" max-width="500" min-width=400>
        <template v-slot:activator="{ props }">
            <v-btn class="tab-btn pa-0 ba-0" v-bind="props" density="compact" block icon="mdi-plus"
            v-shortkey.once="['ctrl', 'n']" @shortkey="showPopup()">
                +
            </v-btn>
        </template>
        <v-card theme="dark" class="mx-auto" min-width="344" title="New Editor">
            <v-form v-model="form">
                <v-container>
                    <v-form v-model="form">
                    <v-text-field variant="solo" density="compact" :readonly="loading" :rules="[required]" v-model="name"
                        label="Name">
                    </v-text-field>
                    <v-divider></v-divider>
                    <v-select variant="solo" density="compact" :readonly="loading" :rules="[required]" v-model="connection"
                        label="Connection" :items="connections" item-title="name">
                    </v-select>
                    <v-divider></v-divider>
                    <v-select variant="solo" density="compact" :readonly="loading" :rules="[required]"
                        v-model="selectedType" label="Type" :items="editorTypes">
                    </v-select>
                </v-form>
                </v-container>
                <v-divider></v-divider>
                <v-alert class="mx-auto square-corners" color="warning" v-if="error">{{ error }}</v-alert>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :disabled="!form" :loading="loading" color="success" @click="localAddEditor">
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
    height: 30px;
    text-transform: none;
    color: var(--text-lighter);
    background-color: var(--main-bg-color);
}
</style>
<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "AddEditorTab",
    data() {
        return {
            form: false,
            loading: false,
            error: '',
            dialog: false,
            connection: null,
            name: '',
            selectedType: 'preql',
            editorTypes: ['preql', 'sql'],

        };
    },
    props: {
    },
    computed: {
        ...mapGetters(['connections', 'getConnectionByName']),
    },
    mounted: () => {
        // console.log(this.connections)
    },
    methods: {
        ...mapActions(['newEditor']),
        showPopup() {
            console.log('showing popup')
            this.dialog = true;
        },
        localAddEditor() {
            const fullConnection = this.getConnectionByName(this.connection)
            this.newEditor({
                name: this.name,
                connection: fullConnection,
                syntax: this.selectedType,
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