<template>
  <div class="cta-container">
    <button :class="{'pill-button': true, 'loading': isSubmitting}" :disabled="isSubmitting">
      {{ buttonText }}
    </button>
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
    isSubmitting: {
      type: Boolean,
      default: false
    }
  },
};
</script>

<style scoped>
.cta-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1em;
}

.pill-button {
  font-size: 1.5em;
  padding: 8px 22px;
  border: solid 1px var(--element-color-2);
  border-radius: 20px;
  color: var(--text-color);
  background-image: linear-gradient(
    to right,
    var(--element-color-1),
    var(--element-color-2)
  );
  cursor: pointer;
  outline: none;
  transition: all 0.3s;
}

.pill-button:hover {
  border: solid 1px var(--highlight-color);
}

.pill-button:disabled {
  cursor: default;
  /* opacity: 0.9; */
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.loading {
  animation: gradient 2s ease infinite;
  background-size: 200% 200%;
}
</style>
