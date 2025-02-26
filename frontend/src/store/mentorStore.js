// store/mentorStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

import { useMessageStore } from "@/store/messageStore";
import { useAuthStore } from '@/store/authStore';
import { usePopupStore } from "@/store/popupStore";

import azaleaImage from '@/assets/images/azalea.png';
import ironaImage from '@/assets/images/irona.png';
import bubblesImage from '@/assets/images/bubbles.png';
import sterlingImage from '@/assets/images/sterling.png';

export const useMentorStore = defineStore('mentorStore', {
    state: () => ({
        mentors: [
            { 
                id: 'azalea', 
                name: 'Azalea', 
                imageUrl: azaleaImage, 
                personality: "<ul><li>Creative and innovative</li><li>Expressive, subtle humor</li><li>Some emojis</li></ul>"
            },
            { 
                id: 'irona', 
                name: 'Irona', 
                imageUrl: ironaImage, 
                personality: "<ul><li>Firm and strict approach</li><li>Effective, dry humor</li><li>Sparse emojis</li></ul>"
            },
            { 
                id: 'bubbles', 
                name: 'Bubbles', 
                imageUrl: bubblesImage, 
                personality: "<ul><li>Playful and lighthearted</li><li>Warm, cheerful jokes</li><li>Lots of emojis</li></ul>"
            },
            { 
                id: 'sterling', 
                name: 'Sterling', 
                imageUrl: sterlingImage, 
                personality: "<ul><li>Professional and direct</li><li>Minimal use of humor</li><li>Almost no emojis</li></ul>"
            },
        ],               
        currentMentor: null,
        selectedMentorName: null,
        isVisible: false,
    }),
    actions: {
        getCurrentMentorName() {
            this.currentMentor = "Azalea"
            const auth = useAuthStore();
            if (!auth.loggedIn){
                return;
            }
            axios.get('/api/mentor')
            .then(response => {
                // console.log(response);
                this.currentMentor = response.data.selectedMentorId;
            })
            .catch(error => {
                console.error('Error fetching selected mentor:', error)
            });
        },
        confirmSelection(name) {
            if (!this.isVisible) { return; }
            const auth = useAuthStore();
            if (!auth.loggedIn){
                const popupStore = usePopupStore();
                popupStore.showPopup(`Sign in to change tutors.`);
                this.hide();
                return;
            }
            this.selectedMentorName = name;
            if (!this.selectedMentorName) {
                this.selectedMentorName = 'Azalea';
            }
            this.hide();
            axios.post('/api/mentor', { mentorId: this.selectedMentorName })
                .then(() => {
                    this.currentMentor = this.selectedMentorName;
                    const path = window.location.pathname;
                    if (path === "/settings"){
                        const popupStore = usePopupStore();
                        popupStore.showPopup(`Mentor personality set to ${this.currentMentor}.<br/>This change will affect the main chat and any new lessons.`);
                    }
                    if (path == "/lessons"){
                        const messageStore = useMessageStore();
                        messageStore.fetchRecentMessages(path);
                    }
                })
                .catch((error) => {                    
                    const popupStore = usePopupStore();
                    popupStore.showPopup(`Error updating mentor selection:${error}`);
                    this.show();
                  });
        },
        show() {
            this.isVisible = true;
            console.log("showed")
        },
        hide() {
            this.isVisible = false;
            console.log("hid")
        },
    },
});
