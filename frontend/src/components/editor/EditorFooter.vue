<template>
    <FooterComponent>
        <template v-if="loading">
            <span class="flex-item">Executing...</span>
            
            <!-- <span class="flex-item">Duration: {{ duration }} ms </span> -->
        </template>
        <template v-else-if='executed'>
            <span class="flex-item">Rows: {{ length }}</span>
            <span class="flex-item">Duration: {{ duration }} ms </span>
        </template>
        <template v-else>
            <span class="flex-item">No Data</span>
        </template>
    </FooterComponent>
</template>
<style scoped>
/* Flex item styles */
.flex-item {
    flex: 1;
    /* Distribute available space evenly among the spans */
    margin-right: 10px;
    /* Optional: Add some spacing between spans */
}

/* Optional: Remove right margin from the last span to avoid extra space */
.flex-item:last-child {
    margin-right: 0;
}
</style>
<script lang="ts">
import { mapGetters } from 'vuex';
import FooterComponent from '/src/components/generic/FooterComponent.vue';
export default {
    name: "EditorFooter",
    components: { FooterComponent },
    props: {
        loading: {
            type: Boolean,
            required: true
        },
        executed: {
            type: Boolean,
            required: true
        },
        length: {
            type: Number,
            required: false
        },
        duration: {
            type: Number,
            required: false
        },
    },
    data: () => ({
        icons: [
        ],
    }),
    computed: {
        ...mapGetters(['activeConnection'])
        // display()
    },
}
</script>