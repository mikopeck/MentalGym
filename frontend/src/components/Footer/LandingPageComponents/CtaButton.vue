<template>
  <div class="cta-container">
    <button class="pill-button">{{ buttonText }}</button>
  </div>
</template>

<script>
export default {
  name: "CtaButton",
  props: {
    buttonText: {
      type: String,
      default: "Start Learning!",
    },
  },
};
</script>

<style scoped>
.cta-container {
  margin-top: 4em;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pill-button {
  font-size: 1.5em;
  margin-top: 1.5em;
  margin-bottom: 1em;
  padding: 15px 30px;
  border: solid 1px var(--element-color-2);
  border-radius: 50px;
  color: var(--text-color);
  background-image: linear-gradient(
    to right,
    var(--element-color-1),
    var(--element-color-2)
  );
  cursor: pointer;
  outline: none;
  transition: border 0.3s;
}

.pill-button:hover {
  border: solid 1px var(--highlight-color);
}
</style>
