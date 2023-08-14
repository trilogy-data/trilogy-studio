<template>
    <v-alert  class="error"
    variant="outlined"
    type="error">
        {{ error }}
    </v-alert>
</template>
<style scoped>
.error {
    border-radius: 0 !important;
}
</style>

<script lang="typescript">
export default {
    name: 'ErrorComponent',
    // data: () => ({
    //     error: null,
    // }), 
    props: {
        error: {
            type: String,
            required: true,
        }
    }
}
</script>