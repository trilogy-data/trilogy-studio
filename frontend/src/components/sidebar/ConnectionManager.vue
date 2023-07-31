<template>
    <div class="connection-manager py-0">
        <v-select class="connection-selector"  density="compact" v-model="selectedConnection"
            :items="connections" item-value="name" item-title="name">
        </v-select>
        <!-- <v-list class="connection-list">
            <template v-for="connection in connections" :key="connection.name">
                <div class="connection-list-item ma-0 pl-10 py-2" @click="setConnection(connection)">
                    <v-icon color="green">mdi-check</v-icon>
                    {{ connection.name }}
                    <template v-slot:append>
                        <v-btn 
                        size="small"
                        density="compact"
                        class="connection-button ma-0 pa-0" 
                        icon="mdi-information" 
                        variant="plain"></v-btn>
                    </template>
                </div>
            </template>
        </v-list> -->
        <!-- <v-btn>Add Connection</v-btn> -->
    </div>
</template>
<style local>
.connection-button .v-field {
    color: var(--text-lighter);
    font-size: 16px;

    height: 10px;
}

.v-field {
    color: var(--text-lighter);
    font-size: 14px;
    background-color: var(--light-bg-color-2);
    height: 44px;
    border-radius: 0;
}

/* vuetify select customizations */
.v-input {
    color: var(--text-lighter);
    font-size: 14px;
    background-color: var(--light-bg-color-2);
    /* height: 30px; */
}

.v-list-item__title {
    color: blue;
}

.v-menu {
    color: var(--text-lighter);
    /* background-color: var(--light-bg-color-2);  */
    font-size: 14px;
}

.connection-selector {
    color: var(--text-lighter) !important;
    background-color: var(--light-bg-color-2);
    /* height:10px; */
    font-size: 80%;
    align-items: left;
    text-align: left;
    border-radius:0px;

}

.connection-list {
    font-size: 80%;
    align-items: left;
    text-align: left;

}

.connection-list-item {
    height: 10px;

}

.connection-manager {
    display: flex;
    flex-direction: row;
    flex-basis: 100%;
    flex-grow: 1;
    flex-shrink: 1;
    flex: 1 1 100%;
    flex-wrap: nowrap;
    width: 100%;
    font-size: .8rem;

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
            selectedConnection: "duckdb_demo"
        };
    },
    computed: {
        ...mapGetters(['activeEditor', 'connections'])
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
