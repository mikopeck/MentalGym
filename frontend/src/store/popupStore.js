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
    showWelcomePopup(){
      this.isVisible = true
      this.message = "Welcome! As you chat with the AI agent, they will build a profile for you and start to offer personalized lessons and challenges. Please keep in mind this app is still in development and contains bugs. If you find any, or just want to share your thoughts, I would greatly appreciate the feedback - there's a contact link in the footer. Or email me directly at miko@ascendance.cloud ."
    }
  }
})
