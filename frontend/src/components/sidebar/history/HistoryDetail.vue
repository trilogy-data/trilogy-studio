

<template>
    <v-dialog v-model="dialog" max-width="500" min-width=400>
        <v-card theme="dark" class="mx-auto" min-width="344" title="History Details">
            <v-container>
            </v-container>
                <v-divider></v-divider>
            <v-alert class="mx-auto square-corners" color="warning" v-if="error">{{ error }}</v-alert>
            <v-card-actions>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<style scoped>
.square-corners {
    border-radius: 0 !important;
}
</style>
<script lang="ts">
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "HistoryDetail",
    data() {

        return {
            form: false,

        };
    },
    props: {
        defaultConnection: {
            type: String,
            default: null,
        },
        dialog: {
            type: Boolean,
            default: false,
        }
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
        ...mapActions(['newEditor', 'setActiveEditor']),
        required(v) {
            return !!v || 'Field is required'
        },
    },
};
</script>