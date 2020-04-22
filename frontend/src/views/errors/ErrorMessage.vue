<template>
  <div>
    <v-container fluid>
      <div id="error-message" class="error--text">
        <h1>{{ code }}</h1>
        <h4>{{ message }}</h4>
        <br />
        <p>{{ url }}</p>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    code: {
      type: Number,
      required: true
    },
    message: {
      type: String,
      required: true
    },
    url: {
      type: String,
      required: false,
      default: ""
    }
  }
});
</script>
