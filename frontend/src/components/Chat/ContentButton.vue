<template>
  <button
    @click="navigateToContent(role)"
    :class="['content-button', isCompleted ? 'completed-button' : '']"
  >
    {{ content }}
    <span class="subtext">Take me there ►</span>
  </button>
</template>

<script>
export default {
  props: {
    content: String,
    role: String,
  },
  methods: {
    navigateToContent(role) {
      this.$emit("navigate", role);
    }
  },
  computed: {
    isCompleted() {
      return String(this.role).includes("?completed");
    },
  },
};
</script>

<style scoped>
.content-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  padding: 0.5rem 1rem;
  background-color: #4a148c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
  position: relative;
}

.content-button .subtext {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 5px;
  transition: color 0.3s ease;
}

.content-button:hover {
  background-color: #6a2bc2;
}

.content-button:hover .subtext {
  color: rgba(255, 255, 255, 0.9);
}

.completed-button {
  opacity: 0.6;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #a7f3c0;
  font-weight: bold;
  position: absolute;
  right: 5px;
  top: 80%;
  transform: translateY(-50%);
}
</style>