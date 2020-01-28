<template>
  <div>
    <h2>{{ feature }}</h2>
    <GuestNameEditor />
  </div>
</template>

<script>
import axios from "axios";
// import { apiService } from "@/common/api.service.js";
import GuestNameEditor from "@/components/GuestNameEditor.vue";
// import Error404ResourceNotFound from "@/views/Error404ResourceNotFound.vue";
export default {
  name: "GuestApp",
  props: {
    feature_slug: {
      type: String,
      required: true
    }
  },
  components: { GuestNameEditor },
  data() {
    return {
      feature: null
    };
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    onModalCloseButtonClicked() {
      this.showModal = false;
    }
    //   async fetchFeatureData() {
    //     this.feature = await apiService(`/api/features/${this.slug}/`);
    //   }
  },
  async beforeRouteEnter(to, from, next) {
    await axios
      .get(`/api/features/${to.params.feature_slug}/`)
      .then(function() {
        next();
      })
      .catch(error => {
        let message = `Feature not found: ${error.config.url}`;
        next(`/not-found/?message=${message}`);
      });
  }
};

// };
</script>

<style></style>
