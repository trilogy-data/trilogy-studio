<template>
    <v-container class="square-corners connection-detail">
        <v-text-field @update:modelValue="updateConnectionName" class="square-corners connection-detail"
            variant="underlined" density="compact" v-model="localName" label="name">
        </v-text-field>
        <v-text-field class="square-corners connection-detail" :type="showKey ? 'text' : 'password'" density="compact"
            :append-icon="showKey ? 'mdi-eye' : 'mdi-eye-off'" @update:modelValue="updateConnectionKey" label="apiKey"
            variant="underlined" v-model="localApiKey" @click:append="showKey = !showKey">
        </v-text-field>
    </v-container>
</template>
<style scoped>
.connection-detail {
    size: 0.8rem;
}

.square-corners {
    border-radius: 0 !important;
}
</style>
<script lang="ts">
import { mapActions, mapGetters } from 'vuex';
import { getConnectionExtras } from './utility.ts';
import { GenAIConnection } from "/src/models/GenAIConnection";
export default {
    name: "AddGenAIConnection",
    data() {
        return {
            showKey: false,
            localApiKey: this.connection?.apiKey,
            localExtra: this.connection?.extra,
            localName: this.connection?.name,
        };
    },
    props: {
        connection: {
            type: GenAIConnection,
            required: false
        }
    },
    computed: {
        ...mapGetters(['models',]),
        extra() {
            return getConnectionExtras(this.selectedType)
        },
    },
    methods: {
        ...mapActions(['addGenAIConnection', 'updateGenAIConnection']),
        showPopup() {
            this.dialog = true;
        },
        submit() {
            this.localAddConnection();
        },
        async updateConnectionName(val) {
            await this.updateGenAIConnection(
                { old: this.connection, new: GenAIConnection.fromJSON({ ...this.connection, 'name': val }) }
            );
        },
        async updateConnectionKey(val) {
            await this.updateGenAIConnection(
                { old: this.connection, new: GenAIConnection.fromJSON({ ...this.connection, 'apiKey': val }) }
            );
        },
        localEditConnection() {
            this.updateGenAIConnection({
                name: this.name,
                provider: this.selectedType,
                extra: this.extraValues,
                apiKey: this.apiKey
            }).then(() => {
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