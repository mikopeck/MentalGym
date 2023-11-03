<template>
  <div class="plan-page">
    <h1 class="page-title">Choose Your Subscription Plan</h1>
    <div class="plans-container">
      <div class="plan" v-for="(plan, index) in plans" :key="index">
        <div class="plan-header" :style="{ backgroundColor: plan.color }">
          <h1>{{ plan.title }}</h1>
          <p class="price">{{ plan.price }}</p>
        </div>
        <div class="plan-body">
          <ul>
            <li v-for="(feature, index) in plan.features" :key="index">
              {{ feature }}
            </li>
          </ul>
        </div>
        <div class="plan-footer">
          <button
            :style="{ backgroundColor: plan.buttonColor }"
            :disabled="userTierMapping[plan.title] === userTier"
            @click="updateUserPlan(plan.title)"
          >
            {{ planButtonLabels[index] }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PlanPage",
  data() {
    return {
      plans: [
        {
          title: "Aspirant",
          price: "Free",
          features: [
            "Personalized mentor. Updated daily.",
            "Custom Lessons & Challenges.",
            "20 Daily Messages.",
          ],
          color: "#4a148c42",
          buttonColor: "#6a34b942",
        },
        {
          title: "Awakened",
          price: "$10/month",
          features: [
            "All features in Aspirant.",
            "Mentor gradually learns about you.",
            "200 daily messages.",
            "Priority Support.",
          ],
          color: "#4a148c82",
          buttonColor: "#4a148c",
        },
        {
          title: "Ascendant",
          price: "$20/month",
          features: [
            "All features in Awakened.",
            "Use the best available AI models.",
            "2000 daily messages",
            "Early access to new features.",
          ],
          color: "#6a34b982",
          buttonColor: "#6a34b9",
        },
      ],
      userTier: "Aspirant",
      userTierMapping: {
        Aspirant: "free",
        Awakened: "paid",
        Ascendant: "pro",
      },
    };
  },
  mounted() {
    this.fetchUserPlan();
  },
  computed: {
    // Computed property to generate the button labels
    planButtonLabels() {
      return this.plans.map((plan) => {
          if (this.userTierMapping[plan.title] === this.userTier) {
              return "Active";
        } else if (this.isUpgrade(plan.title)) {
            return "Upgrade";
        }
        return "Subscribe";
      });
    },
  },
  methods: {
      fetchUserPlan() {
          axios
        .get("/api/plan")
        .then((response) => {
            console.log(response.data)
          this.userTier = response.data.tier;
        })
        .catch((error) => {
          console.error("Error fetching user plan:", error);
        });
    },
    isUpgrade(planTitle) {
      const tierOrder = ["Aspirant", "Awakened", "Ascendant"];
      const currentUserTierIndex = tierOrder.indexOf(
        this.userTierMapping[this.userTier]
      );
      const planTierIndex = tierOrder.indexOf(planTitle);
      return planTierIndex > currentUserTierIndex;
    },
    updateUserPlan(planTitle) {
    axios.post('/api/plan', { tier: this.userTierMapping[planTitle] })
      .then(response => {
        if (response.data.status === 'success') {
          this.userTier = this.userTierMapping[planTitle];
        }
      })
      .catch(error => {
        console.error('Error updating user plan:', error);
      });
  },
  },
};
</script>

<style scoped>
.plan-page {
  color: #f0f8ff;
  background-color: #0e0c14;
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
}

.plans-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.plan-header h1 {
  border-bottom: 2px solid #0e0c14;
}

.plan {
  border: 2px solid #4a148c;
  border-radius: 10px;
  overflow: hidden;
  width: 300px;
  transition: background-color 0.3s;
}

.plan-header {
  padding: 20px;
  color: #f0f8ff;
  text-align: center;
}

.plan:hover {
  background-color: #4a148c82;
}

.plan-body {
  background-color: #4a148c42;
  padding: 12px;
  height: 200px;
}

.plan-footer {
  padding: 20px;
  text-align: center;
  background-color: #6a34b942;
}

.price {
  font-size: 1.5em;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: #f0f8ff;
  cursor: pointer;
  border: 2px solid #4a148c42;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #6a34b942;
}

li {
  padding: 0px;
}

@media (max-width: 768px) {
  .plans-container {
    flex-direction: column-reverse;
    align-items: center;
  }
  .plan {
    width: 100%;
    margin-bottom: 20px;
  }
}
</style>
