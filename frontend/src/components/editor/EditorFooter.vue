<template>
    <FooterComponent>
        <div class="flex-container pa-0 ba-0 result-display">
  <span class="flex-item">Rows {{ length }}</span>
  <span class="flex-item">Duration {{length}} </span>
</div>
        <!-- <div class="result-display px-2 py-0 bg-black text-center w-100">
        <span>
           Rows {{length}} 
        </span>
        <v-spacer></v-spacer>
        <span>
           Duration {{length}} 
        </span> -->
    <!-- </div> -->
    </FooterComponent>
</template>
<style>
.result-display {
    font-size: 0.8rem;
    background-color: black;
    color: var(--text-lighter);
    height:25px;
    border: none;
}

  /* Flex container styles */
  .flex-container {
    display: flex;
  }

  /* Flex item styles */
  .flex-item {
    flex: 1; /* Distribute available space evenly among the spans */
    margin-right: 10px; /* Optional: Add some spacing between spans */
  }

  /* Optional: Remove right margin from the last span to avoid extra space */
  .flex-item:last-child {
    margin-right: 0;
  }

</style>
<script>
import { mapGetters } from 'vuex';
import FooterComponent from '/src/components/generic/FooterComponent.vue';
export default {
    name: "EditorFooter",
    props: {
        length: {
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