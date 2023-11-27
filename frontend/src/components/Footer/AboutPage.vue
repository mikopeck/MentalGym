<template>
  <div class="landing-container">
    <div class="landing-page-1">
      <div class="landing-page">
        <div class="background-gradient-container">
          <div class="content-container">
            <div class="landing-title">Ascendance·☁️</div>
            <div class="buttons">
              <div
                v-for="(item, index) in items"
                :key="index"
                :class="{ 'button-active': activeIndex === index }"
                class="button"
                @click="setActiveIndex(index)"
              >
                {{ item }}
              </div>
            </div>
            <transition name="fade" mode="out-in">
              <div
                class="value-content"
                v-if="activeIndex === 0"
                key="content-0"
              >
                <div class="value-explainer">
                  Personalized AI-driven exploration.
                </div>
                <div class="value-text">
                  Gain experience in a new way. Complete custom lessons, because
                  knowledge is power. Dare to accept challenges tailored to push
                  <i>your</i>
                  limits. Start your Ascendance to reach your potential.
                </div>
              </div>
              <div
                class="value-content"
                v-if="activeIndex === 1"
                key="content-1"
              >
                <div class="value-explainer">
                  Learn anything, challenge yourself.
                </div>
                <div class="value-text">
                  Learn with generated lessons on any topic by a personalized
                  tutor. Engage in quizzes and challenges that adapt to your
                  style, deepening your knowledge and skills.
                </div>
              </div>
              <div
                class="value-content"
                v-if="activeIndex === 2"
                key="content-2"
              >
                <div class="value-explainer">Stats, graphs, streaks...</div>
                <div class="value-text">
                  Seeing progress gives us the rewarding feeling hard work
                  deserves. Track your gains with graphs and stats. Build a
                  habit of growth by keeping up that daily lesson streak.
                </div>
              </div>
            </transition>
            <div class="cta-container" @click="redirectLogin">
              <CtaButton />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="landing-page-2">
      <div class="stat-infos">
        <div class="stat-info">🤝Join 1000+ Ascendants!</div>
        <div class="stat-info">📖12000+ Custom Lessons generated.</div>
        <div class="stat-info">🎯6000+ Personal Challenges accepted.</div>
      </div>
      <div class="faq-container">
        <FaqComponent />
      </div>
    </div>
  </div>
</template>

<script>
import { usePopupStore } from "@/store/popupStore";
import CtaButton from "./LandingPageComponents/CtaButton.vue";
import FaqComponent from "./LandingPageComponents/FaqComponent.vue";

export default {
  name: "AboutPage",
  components: {
    CtaButton,
    FaqComponent,
  },
  data() {
    return {
      items: ["Discover.", "Learn.", "Grow."],
      activeIndex: 0,
      popupMessage: "",
      backgroundImages: [
        require("@/assets/images/discover.webp"),
        require("@/assets/images/learn.webp"),
        require("@/assets/images/grow.webp"),
      ],
    };
  },
  created() {
    const messageCode = this.$route.query.message;
    this.handleMessageCode(messageCode);
    this.interval = setInterval(this.rotateActiveIndex, 6000);
  },
  methods: {
    handleMessageCode(code) {
      const messages = {
        expired_registration_token:
          "This registration token was expired. A new one has been sent to your email.",
        invalid_registration_token:
          "The registration token you provided is invalid. Please check your email for the correct link or contact support.",
      };
      this.popupMessage = messages[code] || "";
      if (this.popupMessage != "") {
        const popupStore = usePopupStore();
        popupStore.showPopup(this.popupMessage);
      }
    },
    redirectLogin() {
      this.$router.push("/login");
    },
    setActiveIndex(index) {
      this.activeIndex = index;
    },
    rotateActiveIndex() {
      this.activeIndex = (this.activeIndex + 1) % this.items.length;
      this.updateBackgroundImage();
    },
    updateBackgroundImage() {
      const landingPage = document.querySelector(".landing-page");
      landingPage.style.backgroundImage = `url(${
        this.backgroundImages[this.activeIndex]
      })`;
    },
    observeStatInfos() {
      const observer = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              observer.unobserve(entry.target);
            }
          });
        },
        {
          threshold: 1,
        }
      );

      const stats = document.querySelectorAll(".stat-info");
      stats.forEach((stat) => {
        observer.observe(stat);
      });
    },
  },
  mounted() {
    this.updateBackgroundImage();
    this.observeStatInfos();
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
};
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.landing-page {
  text-align: left;
  background-repeat: no-repeat;
  background-position: center top;
  background-size: cover;
  transition: background-image 0.5s ease-in-out;
  width: auto;
  height: 84vh;
  max-width: 1024px;
}

.background-gradient-container {
  padding: 0 1em;
  background-image: linear-gradient(
      to top,
      #00000000 90%,
      var(--background-color) 100%
    ),
    linear-gradient(to right, #00000000 90%, var(--background-color) 100%),
    linear-gradient(to left, #00000000 90%, var(--background-color) 100%),
    linear-gradient(to bottom, #00000000 50%, var(--background-color) 95%);
  background-position: center top;
  background-size: cover;
  /* max-width: 1024px; */
  width: 100%;
  height: 84vh;
  z-index: 0;
}

.background-gradient-container::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(var(--background-color-rgb), 0.5);
  z-index: 0;
}

.content-container {
  display: flex;
  height: 100%;
  flex-direction: column;
  justify-content: space-between;
  padding: 0 0.5em;
  position: relative;
  z-index: 1;
}

.landing-title {
  text-align: center;
  font-weight: 700;
  font-size: 4em;
  margin: 1em 0;
  color: var(--text-color);
  text-shadow: 0px 0px 10px var(--background-color),
    0px 0px 20px var(--background-color), 0px 0px 30px var(--background-color);
}

.buttons {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.button {
  display: inline-block;
  cursor: pointer;
  opacity: 0.4;
  margin-right: 10px;
  font-size: 2em;
  text-shadow: none;
  transition: all 0.3s ease;
}

.button-active {
  opacity: 1;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color);
}

.value-content {
  height: 4em;
  font-size: 1.2em;
  transition: all 0.3s ease;
  padding-right: 35%;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color);
}

.value-explainer {
  font-size: 1.2em;
  font-weight: 700;
  transition: all 0.3s ease;
}

.value-text {
  font-size: 1em;
  opacity: 0.85;
  transition: all 0.3s ease;
}

.stat-infos {
  padding: 0.5em;
  text-align: center;
}

.stat-info {
  font-size: 1.2em;
  font-weight: 700;
  margin: 1em;
  opacity: 0;
  transform: translateY(20px);
}

.stat-info.visible {
  animation: fadeSlideIn 0.8s ease-out forwards;
}

.landing-page-1 {
  display: flex;
  justify-content: center;
  height: calc(100vh - 110px);
}
.landing-page-2 {
  display: flex;
  justify-content: center;
  height: calc(100vh - 110px);
  flex-direction: column;
  justify-content: space-around;
}

.faq-container {
  z-index: 1;
}

/* media */

@media only screen and (max-width: 600px) {
    .landing-title {
    font-size: 3em;
  }
  .value-content {
    padding-right: 20%;
  }
  .value-explainer {
    font-size: 1em;
  }
  .value-text {
    font-size: 0.8em;
  }
}

@media only screen and (max-width: 440px) {
  .landing-title {
    font-weight: 700;
    font-size: 2.5em;
  }

  .content-container {
    padding: 0;
  }

  .value-content {
    padding: 0;
  }

  .button {
    font-size: 1.8em;
  }

  .cta-container {
    padding-top: 1em;
  }
}

@media only screen and (max-width: 350px) {
  .landing-title {
    font-size: 2em;
  }
}

@media only screen and (max-height: 660px) {
  .landing-title {
    margin: 0;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
