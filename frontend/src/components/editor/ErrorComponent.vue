<template>
    <v-alert  class="error"
    variant="outlined"
    type="error">
    <div class = "error-message-container">
        {{ error }}
    </div>
    </v-alert>
</template>
<style scoped>
.error {
    border-radius: 0 !important;
}

.error-message-container {
  overflow-y: auto; /* Enable vertical scrolling */
}

.scrollable-text {
  margin: 0;
  padding: 8px;
}
</style>

<script lang="ts">
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