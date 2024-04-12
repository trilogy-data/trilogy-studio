

<template>
    <v-dialog class="override-style" v-model="dialog" max-width="500" min-width=400>
        <template v-slot:activator="{ props }">
            <v-btn class="sidebar-detail-btn square-corner"  v-bind="props" :density="density" 
            icon="mdi-edit"
             >
                Edit
            </v-btn>
        </template>
        <v-card theme="dark" class="mx-auto" min-width="344" :title="`Update ${name}`">
            <v-form v-model="form">
                <v-container>
                    <v-form v-model="form">
                        <v-select variant="solo" density="compact" :readonly="loading" :rules="[required]"
                            v-model="connection" label="Connection" :items="connections" item-title="name">
                        </v-select>
                        <!-- <v-divider></v-divider>
                        <v-select variant="solo" density="compact" :readonly="loading" :rules="[required]"
                            v-model="selectedType" label="Type" :items="editorTypes">
                        </v-select> -->
                    </v-form>
                </v-container>
                <v-divider></v-divider>
                <v-alert class="mx-auto square-corners" color="warning" v-if="error">{{ error }}</v-alert>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn  type="submit" :disabled="!form" :loading="loading" color="success" @click="localAddEditor">
                        Save
                        <v-icon icon="mdi-chevron-right" end></v-icon>
                    </v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
    </v-dialog>
</template>
<style scoped>
.override-style {
  display: 'auto';
  width: '100%';
}

</style>
<script lang="ts">
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "EditEditorPopup",
    data() {

        return {
            form: false,
            loading: false,
            error: '',
            dialog: false,
            connection: this.defaultConnection,
            // selectedType: 'preql',
            // editorTypes: ['preql', 'sql'],

        };
    },
    props: {
        defaultConnection: {
            type: String,
            default: null,
           
        },
        density: String,
        name: String
    },
    computed: {
        ...mapGetters(['connections', 'getConnectionByName', 'unconnectedLabel']),
        label() {
            return this.name ? this.name : 'New Editor'
        },
        allowedConnections() {
            return this.connections.filter((c) => c.name != this.unconnectedLabel)
        }
    },
    methods: {
        ...mapActions(['editEditor', 'setActiveEditor']),
        showPopup() {
            this.dialog = true;
        },
        localAddEditor() {
            const fullConnection = this.getConnectionByName(this.connection)
            this.editEditor({
                name: this.name,
                connection: fullConnection,
            }).then(() => {
                this.setActiveEditor(this.name).then(() => {
                    this.dialog = false;
                })

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