<template>
  <div class="center-content">
    <div class="background-gradient-container">
      <div class="about-main-container">
        <div class="reactive-subtitle">
          <h1>Unlock Your Potential with Ascendance·☁️</h1>
        </div>
        <div class="about-main-section">
          <h3>Discover, Experience, Grow</h3>
          <div class="ascent-container">
            <button class="ascent-button" @click="redirectLogin">
              Begin your ascent
            </button>
          </div>
          <p>
            As sentient civilizations uncover more laws of the universe and
            escape the gravity wells of their planets, the astonishing abundance
            of resources becomes apparent. We believe in the limitless potential
            of every sentient individual. Our mission is to empower you to
            ascend to new heights in your personal and professional endeavors.
            Make your life meaningful. Create memories. The AI in this app is
            designed to help you succeed if you know exactly what you want to
            achieve, but also to offer guidance and suggest a path when you
            feel lost in life.
          </p>
          <div class="reactive-subtitle"><h2>🛠How We Work</h2></div>
          <ul>
            <li>
              <div class="reactive-subtitle">📖Intelligent Tutoring</div>
              Our platform features a sophisticated AI chat interface that
              learns about you — your strengths, weaknesses, goals, and
              aspirations. It then suggests and tailors lessons and challenges
              uniquely suited to your style.
            </li>
            <li>
              <div class="reactive-subtitle">📚Diverse Learning Topics</div>
              Whether you're diving into quantum physics, exploring the world of
              digital art, or brushing up on ancient history, we've got you
              covered. Our AI curates lessons on virtually any topic you're
              passionate about.
            </li>
            <li>
              <div class="reactive-subtitle">🎯Personalized Challenges</div>
              Beyond lessons, we present challenges that push your boundaries
              and test your understanding, ensuring you're always growing and
              progressing.
            </li>
            <li>
              <div class="reactive-subtitle">🌱Mentorship</div>
              More than just a tutor, our AI acts as a mentor, guiding you,
              motivating you, and celebrating your achievements with you.
            </li>
          </ul>

          <div class="reactive-subtitle"><h2>👀Our Vision</h2></div>
          Our future is one where AI empowers human excellence and flourishing.
          This whole app is inspired and driven by the ideas in
          <a href="https://arxiv.org/pdf/2302.09248.pdf">this paper</a>.

          <div class="reactive-subtitle">
            <h2>🤖Technology Behind the Scenes</h2>
          </div>
          <p>
            Harnessing the power of the latest AI models, we've created a
            seamless and adaptive learning experience. Our algorithms are
            constantly evolving, ensuring the lessons and challenges remain
            relevant and effective for you.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { usePopupStore } from "@/store/popupStore";
export default {
  name: "AboutPage",
  data() {
    return {
      popupMessage: "",
    };
  },
  created() {
    const messageCode = this.$route.query.message;
    this.handleMessageCode(messageCode);
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
  },
};
</script>

<style scoped>
.about-main-container {
  font-weight: 500;
    margin-top: 1em;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.center-content {
  max-width: 1024px;
  margin: auto;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.background-gradient-container {
  position: relative;
  background-image: linear-gradient(
      to right,
      #00000000 90%,
      var(--background-color) 100%
    ),
    linear-gradient(to left, #00000000 90%, var(--background-color) 100%),
    linear-gradient(to bottom, #00000000 60%, var(--background-color) 100%),
    url("~@/assets/images/background_hued_web.png");
  background-position: center top;
  background-size: cover;
  max-width: 1024px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.background-gradient-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(var(--background-color-rgb), 0.4);
  z-index: 0;
}

@media (max-width: 768px) {
  .center-content, .background-gradient-container {
    max-width: 100%;
  }}
.about-main-container {
  z-index: 1;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color);
}

.ascent-button {
  position: relative;
  background: radial-gradient(
    ellipse at center,
    #bb86fcb8 20%,
    transparent 80%
  );
  font-size: 1.4em;
  margin-top: 8px;
  padding: 10px 15px;
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: text-shadow 0.3s ease;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color);
  transform-origin: 50% 50%;
}

.ascent-button:hover {
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
}
@keyframes wiggle {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-20px);
  }
}

.ascent-button:hover {
  animation: wiggle 10s infinite;
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
}

.ascent-button::before {
  content: "→";
  left: calc(-100% - 10px);
}
.ascent-button::after {
  right: calc(-100% - 10px);
  content: "←";
}
.ascent-button::before,
.ascent-button::after {
  font-weight: 900;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  opacity: 1;
  transition: opacity 0.3s ease;
}

.ascent-button::before {
  left: -20px;
  animation: arrow-motion-before 2s linear infinite alternate;
}

.ascent-button::after {
  right: -20px;
  animation: arrow-motion-after 2s linear infinite alternate;
}

@keyframes arrow-motion-before {
  0% {
    transform: translateY(-50%) translateX(0);
  }
  100% {
    transform: translateY(-50%) translateX(-10px);
  }
}

@keyframes arrow-motion-after {
  0% {
    transform: translateY(-50%) translateX(0);
  }
  100% {
    transform: translateY(-50%) translateX(10px);
  }
}

.ascent-button:hover::before,
.ascent-button:hover::after {
  opacity: 0;
}

.reactive-subtitle {
  font-weight: 700;
  position: relative;
  transition: opacity 0.3s ease;
}

.reactive-subtitle::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: radial-gradient(
    ellipse at center,
    #bb86fc42 20%,
    transparent 80%
  );
  opacity: 0;
  transition: opacity 0.2s ease;
}

.reactive-subtitle:hover::after {
  opacity: 1;
}

h1,
h2 {
  margin-top: 20px;
}

p {
  margin: 10px 0;
}

.ascent-container {
  text-align: center;
}
</style>
