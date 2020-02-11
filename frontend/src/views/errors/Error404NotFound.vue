<template>
  <div>
    <div class="container mt-3">
      <div id="error-message">
        <h1>404</h1>
        <h5>{{ message }}</h5>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "error-404-not-found",
  props: {
    message: {
      type: String,
      required: true
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
