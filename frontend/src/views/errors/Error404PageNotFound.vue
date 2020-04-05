<template>
  <error-message
    heading="404"
    message="Page not found."
    :url="url ? url : $route.fullPath"
  />
</template>

<script>
import ErrorMessage from "@/views/errors/ErrorMessage.vue";

export default {
  name: "Error404PageNotFound",
  components: { ErrorMessage },
  props: {
    url: {
      type: String,
      required: false,
      default: null
    }
  }
};
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
