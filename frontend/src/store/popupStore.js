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
    showLibraryInstructions(){
      this.isVisible = true
      this.message = "<h4>Welcome to Ascendance·☁️</h4><div style='text-align: left;'><br/><ul><li>Explore the Library rooms</li><li>The central room is already unlocked</li><li>Find interesting facts in bookshelves indicated by *<b>!</b>*</li><li>Answer questions indicated by *<b>?</b>* to unlock adjacent rooms</li><li>Keep a correct answer streak to gain maximum score!</li><li>This app is still in development and may contain bugs</li><li>Any <a href='/contact' target='_blank'>feedback</a> is greatly appreciated </li></ul></div>"
    },
    showLibraryCompletionInfo(){
      this.isVisible = true
      this.message = "<h1>You can now complete the library!</h1><h4>Keep going to gain maximum points!</h4><h4>Click the score once you are ready.</h4>"
    }
  }
})
