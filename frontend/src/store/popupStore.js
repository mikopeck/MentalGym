// store/popupStore.js
import { defineStore } from 'pinia'

export const usePopupStore = defineStore('popup', {
  // state
  state: () => ({
    isVisible: false,
    message: '',
  }),
  // actions
  actions: {
    showPopup(message) {
      this.isVisible = true
      this.message = message
    },
    hidePopup() {
      this.isVisible = false
      this.message = ''
    },
    showWelcomePopup() {
      this.isVisible = true
      this.message = "Welcome to Ascendance·☁️!<br/>As you chat with your AI mentor, they will build a profile for you and offer personalized lessons. Please keep in mind this app is still in development and may contain bugs. If you find any, or just want to share your thoughts, I would greatly appreciate your <a href='/contact'>feedback</a>."
    }
  }
})
