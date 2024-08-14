<template>
  <div class="library-browser">
    <LibraryCarousel title="My Libraries" :libraries="myLibraries" v-if="loggedIn & browsingLibraries"/>
    <LibraryCarousel
      title="Most Liked Libraries"
      :libraries="mostLikedLibraries"
    />
    <LibraryCarousel title="Newest Libraries" :libraries="newestLibraries" />
  </div>
</template>

<script>
import axios from "axios";

import { useAuthStore } from "@/store/authStore";
import LibraryCarousel from "./LibraryCarousel.vue";

export default {
  name: "LibraryBrowser",
  components: {
    LibraryCarousel,
  },
  data() {
    return {
      myLibraries: [],
      mostLikedLibraries: [],
      newestLibraries: [],
    };
  },
  mounted() {
    this.fetchLibraries();
  },
  methods: {
    fetchLibraries() {
      axios
        .get("/api/libraries")
        .then((response) => {
          this.mostLikedLibraries = response.data.most_liked;
          this.newestLibraries = response.data.latest;

          if (this.loggedIn){
            this.myLibraries = response.data.mine;
          }
        })
        .catch((error) => {
          console.error("Failed to fetch libraries", error);
        });
    },
  },
  computed: {
    loggedIn(){
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
    browsingLibraries(){
      return this.$route.path == "/library"
    }
  }
};
</script>

<style scoped>
.library-browser {
  width: 98%;
}
</style>
