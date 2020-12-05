<template>
  <div>
    <v-snackbar :color="currentNotificationType" v-model="show" bottom>
      <v-row align="center" justify="center">
        <v-progress-circular
          size="24"
          class="ma-5"
          v-show="showProgress"
          indeterminate
        ></v-progress-circular>
        <v-icon class="ma-5" v-show="!showProgress">
          {{ currentNotificationIcon }}
        </v-icon>
        {{ currentNotificationContent }}
        <v-spacer></v-spacer>
        <v-btn @click.native="close" class="ma-2" icon>
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-row>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { AppNotification } from "@/store/main/state";
import { commitRemoveNotification } from "@/store/main/mutations";
import { readFirstNotification } from "@/store/main/getters";
import { dispatchRemoveNotification } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      show: false as boolean,
      text: "" as string,
      showProgress: false as boolean,
      currentNotification: false as AppNotification | false,
    };
  },
  methods: {
    async hide() {
      this.show = false;
      await new Promise((resolve) => setTimeout(() => resolve({}), 500));
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
    async setNotification(notification: AppNotification | false) {
      if (this.show) {
        await this.hide();
      }
      if (notification) {
        this.currentNotification = notification;
        this.showProgress = notification.showProgress || false;
        this.show = true;
      } else {
        this.currentNotification = false;
      }
    },
  },
  computed: {
    firstNotification() {
      return readFirstNotification(this.$store);
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
    firstNotification: async function (
      newNotification: AppNotification | false,
      oldNotification: AppNotification | false
    ) {
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
