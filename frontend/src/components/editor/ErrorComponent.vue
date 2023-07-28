<template>
    <v-alert>
        {{ error }}
    </v-alert>
</template>


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