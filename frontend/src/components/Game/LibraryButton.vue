<template>
  <button class="library-button">
    {{ library.library_topic }}
  </button>
</template>

<script>
export default {
  name: 'LibraryButton',
  props: {
    library: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.library-button {
  padding: 10px 20px;
  margin: 5px;
  background-color: var(--element-color-1);
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.library-button:hover {
  background-color: var(--element-color-2);
}
</style>
