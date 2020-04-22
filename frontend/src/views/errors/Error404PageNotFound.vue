<template>
  <div>
    <error-message :code="code" message="Page not found." :url="url ? url : $route.fullPath" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import ErrorMessage from "@/views/errors/ErrorMessage.vue";

export default Vue.extend({
  name: "Error404PageNotFound",
  components: { ErrorMessage },
  props: {
    url: {
      type: String,
      required: false,
      default: null
    }
  },
  data() {
    return {
      code: 404
    };
  }
});
</script>

<style scoped>
#error-message {
  color: red;
  text-align: center;
}
#error-detail {
  color: black;
  text-align: center;
}
</style>
