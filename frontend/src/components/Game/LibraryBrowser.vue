<template>
  <div class="library-browser">
    <LibraryCarousel
      title="Most Liked Libraries"
      :libraries="mostLikedLibraries"
    />
    <LibraryCarousel title="Newest Libraries" :libraries="newestLibraries" />
  </div>
</template>

<script>
import axios from "axios";
import LibraryCarousel from "./LibraryCarousel.vue";

export default {
  name: "LibraryBrowser",
  components: {
    LibraryCarousel,
  },
  data() {
    return {
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
        })
        .catch((error) => {
          console.error("Failed to fetch libraries", error);
        });
    },
  },
};
</script>

<style scoped>
.library-browser {
  width: 98%;
}
</style>
