// store/mentorStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

import { useMessageStore } from "@/store/messageStore";
import { usePopupStore } from "@/store/popupStore";

import azaleaImage from '@/assets/images/azalea.png';
import ironaImage from '@/assets/images/irona.png';
import bubblesImage from '@/assets/images/bubbles.png';
import sterlingImage from '@/assets/images/sterling.png';

export const useMentorStore = defineStore('mentorStore', {
    state: () => ({
        mentors: [
            { id: 'azalea', name: 'Azalea', imageUrl: azaleaImage },
            { id: 'irona', name: 'Irona', imageUrl: ironaImage },
            { id: 'bubbles', name: 'Bubbles', imageUrl: bubblesImage },
            { id: 'sterling', name: 'Sterling', imageUrl: sterlingImage },
        ],
        currentMentor: null,
        selectedMentorId: null,
        isVisible: false,
    }),
    actions: {
        getCurrentMentorName() {
            axios.get('/api/mentor')
                .then(response => {
                    console.log(response);
                    this.currentMentor = response.data.selectedMentorId;
                })
                .catch(error => console.error('Error fetching selected mentor:', error));
        },
        selectMentor(mentorId) {
            this.selectedMentorId = mentorId;
        },
        confirmSelection() {
            if (this.isVisible === false) { console.log("wowww"); return; }
            this.hide();
            axios.post('/api/mentor', { mentorId: this.selectedMentorId })
                .then(() => {
                    this.currentMentor = this.selectedMentorId;
                    console.log(this.selectedMentorId);
                    const popupStore = usePopupStore();
                    popupStore.showPopup(`Mentor personality set to ${this.currentMentor}.<br/>This change will affect the main chat and any new lessons or challenges.`);
                    const messageStore = useMessageStore();
                    const path = window.location.pathname;
                    messageStore.fetchRecentMessages(path);
                    return;
                })
                .catch((error) => {                    
                    const popupStore = usePopupStore();
                    popupStore.showPopup(`Error updating mentor selection:${error}`);
                    this.show();
                  });
        },
        show() {
            this.isVisible = true;
        },
        hide() {
            this.isVisible = false;
        },
    },
});
