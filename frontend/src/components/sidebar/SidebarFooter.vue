<template>
    <FooterComponent>
        <div v-if="activeEditor" class="connection-display px-2 py-0 bg-black text-center w-100">
            {{activeEditor.connection.name}} — <strong>{{activeEditor.connection.type}}</strong>
        </div>
    </FooterComponent>
</template>
<style>
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
<script>
import { mapGetters } from 'vuex';
import FooterComponent from '/src/components/generic/FooterComponent.vue';
export default {
    name: "EditorFooter",
    data: () => ({
        icons: [
            'mdi-facebook',
            'mdi-twitter',
            'mdi-linkedin',
            'mdi-instagram',
        ],
    }),
    computed: {
        ...mapGetters(['activeEditor'])
    },
}
</script>