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
      this.message = "<h4>Welcome to Ascendance·☁️</h4><div style='text-align: left;'><br/><ul><li>Chat with your tutor to create a profile</li><li>Start learning through personalized lessons</li><li>Complete quizzes to build your Knowledge Map</li><li>This app is still in development and may contain bugs</li><li>Any <a href='/contact' target='_blank'>feedback</a> is greatly appreciated </li></ul></div>"
    },
    showLibraryInstructions() {
      this.isVisible = true
      this.message = "<h4>Welcome to Ascendance·☁️</h4><div style='text-align: left;'><br/><ul><li>Answer questions to explore the library.</li><li>Tap a question to learn more.</li><li>After four complete rooms, a final room can appear.</li><li>Complete the final room to start a daily streak and gain levels!</li><li>This app is still in development and may contain bugs.</li><li>Any <a href='/contact' target='_blank'>feedback</a> is greatly appreciated </li></ul></div>"
    },
  }
})
