<template>
  <div class="d-flex align-center justify-center">
    <v-alert
      :type="currentNotificationType"
      v-model="show"
      :prominent="true"
      dismissible
      class="ma-5 mx-sm-16"
    >
      <template v-slot:prepend v-if="showProgress">
        <v-progress-circular class="ma-5" indeterminate></v-progress-circular>
      </template>
      <v-icon class="ma-5" v-else> mdi-close </v-icon>

      <v-col class="align-self-center">
        {{ currentNotificationContent }}
      </v-col>
    </v-alert>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "@/store";
import { AppNotification } from "@/store/main/state";
import { commitRemoveNotification } from "@/store/main/mutations";
import { readFirstNotification, readNotifications } from "@/store/main/getters";
import { dispatchRemoveNotification } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      show: false as boolean,
      text: "" as string,
      showProgress: false as boolean,
      currentNotification: null as AppNotification | null,
    };
  },
  methods: {
    async hide() {
      await new Promise((resolve) => setTimeout(() => resolve({}), 500));
      this.show = false;
    },
    async close() {
      await this.hide();
      await this.removeCurrentNotification();
    },
    async removeCurrentNotification() {
      if (this.currentNotification) {
        commitRemoveNotification(this.$store, this.currentNotification);
      }
    },
    async setNotification(notification: AppNotification | null) {
      if (this.show) {
        await this.hide();
      }
      if (notification) {
        this.currentNotification = notification;
        this.showProgress = notification.showProgress || false;
        this.show = true;
      } else {
        this.currentNotification = null;
      }
    },
  },
  computed: {
    firstNotification() {
      return readFirstNotification(store);
    },
    currentNotificationContent() {
      return (
        (this.currentNotification && this.currentNotification.content) || ""
      );
    },
    currentNotificationType() {
      return (
        (this.currentNotification && this.currentNotification.type) || "info"
      );
    },
    currentNotificationIcon() {
      if (!this.currentNotification) {
        return null;
      } else if (this.currentNotification.type === "success") {
        return "mdi-check-circle";
      } else if (this.currentNotification.type === "info") {
        return "mdi-information-outline";
      } else if (this.currentNotification.type === "warning") {
        return "mdi-alert-outline";
      } else if (this.currentNotification.type === "error") {
        return "mdi-alert-octagon-outline";
      } else {
        return "checkbox-blank-circle";
      }
    },
  },
  watch: {
    firstNotification: async function (newNotification: AppNotification) {
      if (newNotification !== this.currentNotification) {
        this.setNotification(newNotification);
        if (newNotification) {
          dispatchRemoveNotification(this.$store, {
            notification: newNotification,
            timeout: 6500,
          });
        }
      }
    },
  },
});
</script>
