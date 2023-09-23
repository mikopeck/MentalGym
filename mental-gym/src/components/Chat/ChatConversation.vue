<template>
    <div id="conversation">
      <div v-for="message in messages" :key="message.id" :class="message.role" class="fade-in">
        <p v-if="message.role !== 'system'">{{ message.content }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      messages: Array
    }
  }
  </script>
  
  <style scoped>
.fade-in {
  transition: all 0.3s ease;
}

.user {
  @apply bg-green-200 text-green-700 rounded-br-none rounded-bl-lg rounded-t-lg text-left my-2 p-2 w-3/4 float-left;
}

.assistant {
  @apply bg-purple-200 text-purple-700 rounded-bl-none rounded-br-lg rounded-t-lg text-right my-2 p-2 w-3/4 float-right;
}

@keyframes slideInFromBottom {
  0% {
    transform: translateY(100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.fade-in {
  animation: slideInFromBottom 0.3s forwards;
}
</style>
