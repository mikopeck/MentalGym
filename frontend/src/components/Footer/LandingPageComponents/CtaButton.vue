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
  position: relative;
  font-size: 1.5em;
  padding: 8px 22px;
  border: 2px solid var(--element-color-2);
  border-radius: 20px;
  color: var(--text-color);
  background-color: var(--element-color-1);
  cursor: pointer;
  outline: none;
  transition: all 0.3s;
  z-index: 1;
  overflow: hidden;
}

.pill-button::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    90deg,
    var(--element-color-1),
    var(--highlight-color),
    var(--element-color-2),
    var(--element-color-1)
  );
  background-size: 200% 200%;
  border-radius: inherit;
  z-index: -1;
  filter: blur(4px);
  opacity: 0;
  transition: opacity 0.3s;
}

.pill-button:hover {
  border-color: var(--highlight-color);
}

.pill-button:disabled {
  cursor: default;
}

.pill-button.loading::before {
  opacity: 1;
  animation: gradientBorder 4s linear infinite;
}

@keyframes gradientBorder {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}
</style>

