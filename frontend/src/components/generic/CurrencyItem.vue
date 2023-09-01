<template>
    <span>
        {{ value.currency }}{{ Math.round(value.value * 100) / 100 }}
    </span>
</template>
<script lang="ts">
export default {
    name: "CurrencyItem",
    props: {
        value: {
            type: Object,
            required: true
        },
    },
};
</script>