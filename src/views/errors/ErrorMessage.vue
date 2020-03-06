<template>
  <div>
    <v-container fluid>
      <div id="error-message" class="error--text">
        <h1>{{ heading }}</h1>
        <h4>{{ message }}</h4>
        <br />
        <p>{{ url }}</p>
      </div>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "base-error-message",
  props: {
    heading: {
      type: String,
      required: false,
      default: "Error"
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
};
</script>
