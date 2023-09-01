<template>
    <FooterComponent>
        <div v-if="connection" class="connection-display px-2 py-0 bg-black text-center w-100">
            {{ name }} — <strong>{{ type }}</strong>
        </div>
    </FooterComponent>
</template>
<style scoped>
.footer {
    --height: 25px;
    height: var(--height);
    min-height: var(--height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;


}

.connection-display {
    font-size: 0.8rem;
}
</style>
<script lang="ts">
import { mapGetters } from 'vuex';
import FooterComponent from '/src/components/generic/FooterComponent.vue';
import { Connection } from '/src/models/Connection';
export default {
    name: "EditorFooter",
    components: { FooterComponent },
    computed: {
        ...mapGetters(['activeEditor', 'getConnectionByName']),
        connection() {
            // @ts-ignore
            let conn = this.activeEditor.connection
            if (!conn) return null;
            // @ts-ignore
            let connection: Connection = this.getConnectionByName(conn) as Connection
            return connection
        },
        name() {
            if (this.connection) {
                return this.connection.name
            }
        },
        type() {
            if (this.connection) {
                return this.connection.type
            }
        }
    },
}
</script>