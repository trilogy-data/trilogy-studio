<template>
    <footer class="d-flex flex-row pa-0 ba-0 footer row">
        <slot/>
    </footer>
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
</style>
<script>
import { mapGetters } from 'vuex';
export default {
    name: "FooterComponent",
    data: () => ({
        icons: [
        ],
    }),
}
</script>