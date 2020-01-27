<template>
  <div>
    <h2>{{ feature }}</h2>
    <GuestNameEditor />
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import GuestNameEditor from "@/components/GuestNameEditor.vue";
export default {
  name: "GuestApp",
  props: {
    slug: {
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
  created() {
    this.fetchFeatureData();
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    onModalCloseButtonClicked() {
      this.showModal = false;
    },
    async fetchFeatureData() {
      this.feature = await apiService(`/api/features/${this.slug}/`);
    }
  }
};
</script>

<style></style>
