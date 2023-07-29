<template>
    <div class="connection-manager">
        <div class='title'>Active Connection: {{ activeEditor }}</div>
        <v-list class="connection-list">
            <template v-for="connection in connections" :key="connection.name">
                <v-list-item @click="setConnection(connection)">
                    <template v-slot:prepend>
                        <v-icon>mdi-check</v-icon>
                    </template>
                    {{ connection.name }}
                </v-list-item>
            </template>
        </v-list>
        <v-btn>Add Connection</v-btn>
    </div>
</template>
<style local>
.connection-manager {
    display: flex;
    flex-direction: row;
    flex-basis: 100%;
    flex-grow: 1;
    flex-shrink: 1;
    flex: 1 1 100%;
    flex-wrap: nowrap;
    width: 100%;
}

.title {
    color: var(--text-lighter);
    font-size: 95%;
    margin-bottom: 5px;
}

.connection-list {
    background-color: var(--main-bg-color);
}
</style>
<script>

import instance from '../../api/instance';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "ConnectionManager",
    data() {
        return {
            connections: [
                { 'name': 'duckdb' },
                { 'name': 'bigquery' }
            ]
        };
    },
    computed: {
        ...mapGetters(['activeEditor'])
    },
    methods: {
        ...mapActions(['setActiveConnection']),
        setConnection(conn) {
            this.setActiveConnection(conn.name)
            console.log(`connection set to ${conn.name}`)
        },
        addConnection() {
            let local = this;
            return instance.post('connection', {
            }).then(() => {
                console.log('add connection')

            })
        },
        removeConnection() {
            let local = this;
            return instance.post('connection', {
            }).then(() => {
                console.log('add connection')

            })
        },
        loadConnections() {
            let local = this;
            return instance.get('connections', {
            }).then((response) => {
                this.connections = response.connections

            })
        },
    },
    mounted() {
        //    this.loadConnections()
    },
};
</script>
