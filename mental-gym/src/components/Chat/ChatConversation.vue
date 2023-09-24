<template>
  <br/>
  <br/>
  <br/>
  <br/>
  <br/>
  <br/>
  <div id="conversation">
    <div v-for="message in messages" :key="message.id" :class="message.role" class="chat-bubble fade-in">
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
.chat-bubble {
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  width: 75%;
  transition: all 0.3s ease-in-out;
  border-top-right-radius: 7px;
  border-top-left-radius: 7px;
}

.user {
  float: left;
  text-align: left;
  background-color: rgba(167, 243, 208, 0.4);
  box-shadow: 0 0 4px 4px rgba(167, 243, 208, 0.4);
  border-bottom-right-radius: 7px;
}

.assistant {
  float: right;
  text-align: right;
  background-color: rgba(221, 214, 254, 0.4);
  box-shadow: 0 0 4px 4px rgba(221, 214, 254, 0.4);
  border-bottom-left-radius: 7px;
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
