import { reactive } from 'vue';

const eventBus = reactive({
  emit(event, ...args) {
    this[event]?.(...args);
  },
  on(event, callback) {
    this[event] = callback;
  },
  off(event) {
    delete this[event];
  }
});

export default eventBus;
