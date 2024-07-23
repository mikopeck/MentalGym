<template>
  <div class="plan-page">
    <h1 class="page-title" v-if="isPlanPage">Choose Your Subscription Plan</h1>
    <h1 class="page-title">Subscription Plans</h1>
    <div class="plans-container">
      <div class="plan" v-for="(plan, index) in plans" :key="index">
        <div class="plan-header" :style="{ backgroundColor: plan.color }">
          <h1 v-if="loggedIn">{{ plan.title }}</h1>
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

import { useAuthStore } from '@/store/authStore';

export default {
  name: "PlanPage",
  data() {
    return {
      plans: [
        {
          title: "Aspirant",
          price: "Free",
          features: [
            "10☁️ Free Every Day",
            "Custom Libraries",
            "Knowledge Map",
            "Personal Tutor",
          ],
          color: "var(--background-color-1t)",
          buttonColor: "var(--background-color-2t)",
        },
        {
          title: "Awakened",
          price: "$4/month",
          features: [
            "100☁️Every Day",
            "All features in Aspirant",
            "Unlimited Knowledge Map",
            "Priority Support",
          ],
          color: "var(--element-color-1)",
          buttonColor: "var(--element-color-1)",
        },
        {
          title: "Ascendant",
          price: "$8/month",
          features: [
            '1000☁️ Every Day',
            "All Features in Awakened",
            "Use Frontier AI Models",
            "Early Access to New Features",
          ],
          color: "var(--element-color-2)",
          buttonColor: "var(--element-color-2)",
        },
      ],
      userTierMapping: {
        Aspirant: "free",
        Awakened: "paid",
        Ascendant: "pro",
      },
      planUrls: {
        Aspirant: "https://buy.stripe.com/bIY6sg5154ZmaXu4gi",
        Awakened: "https://buy.stripe.com/cN2aIw79ddvSghOaEI",
        Ascendant: "https://buy.stripe.com/9AQ5ocbptfE0fdK005",
      },
    };
  },
  computed: {
    isPlanPage() {
      return this.$route.path === "/plan";
    },
    authStore(){
      return useAuthStore();
    },
    loggedIn(){
      return this.authStore.loggedIn;
    },
    userTier() {
      return this.authStore.userTier;
    },
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
          this.userTier = response.data.tier;
        })
        .catch((error) => {
          console.error("Error fetching user plan:", error);
        });
    },
    isUpgrade(planTitle) {
      const tierOrder = ["Aspirant", "Awakened", "Ascendant"];
      const currentUserTierIndex = tierOrder.indexOf(
        Object.keys(this.userTierMapping).find(
          (key) => this.userTierMapping[key] === this.userTier
        )
      );
      const planTierIndex = tierOrder.indexOf(planTitle);
      return planTierIndex > currentUserTierIndex;
    },
    updateUserPlan(planTitle) {
      const paymentUrl = this.planUrls[planTitle];
      window.open(paymentUrl, "_blank");
      axios
        .post("/api/plan", { tier: this.userTierMapping[planTitle] })
        .then((response) => {
          if (response.data.status === "success") {
            this.userTier = this.userTierMapping[planTitle];
          }
        })
        .catch((error) => {
          console.error("Error updating user plan:", error);
        });
    },
  },
};
</script>

<style scoped>
.plan-page {
  color: var(--text-color);
  background-color: var(--background-color);
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
  border-bottom: 2px solid var(--background-color);
}

.plan {
  border: 2px solid var(--element-color-1);
  border-radius: 8px;
  overflow: hidden;
  width: 300px;
  opacity: 1;
  background-color: #00000000;
  transition: background-color opacity 0.3s;
}

.plan-header {
  padding: 20px;
  color: var(--text-color);
  text-align: center;
}

.plan:hover {
  background-color: var(--element-color-1);
  opacity: 0.8;
}

.plan-body {
  background-color: var(--background-color-1t);
  padding: 12px;
  height: 200px;
}

.plan-footer {
  padding: 20px;
  text-align: center;
  background-color: var(--background-color-2t);
}

.price {
  font-size: 1.5em;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  color: var(--text-color);
  cursor: pointer;
  border: 2px solid var(--background-color-1t);
  transition: background-color 0.3s;
}

button:hover {
  background-color: var(--background-color-2t);
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
