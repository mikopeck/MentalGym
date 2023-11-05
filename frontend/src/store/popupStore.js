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
    }
  }
})
