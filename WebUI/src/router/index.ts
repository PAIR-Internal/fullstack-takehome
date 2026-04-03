import { createRouter, createWebHistory } from "vue-router";

const LearnerWorkspaceView = () =>
  import("@/domains/learnerProgress/views/LearnerWorkspaceView.vue");

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "learner-workspace",
      component: LearnerWorkspaceView,
    },
  ],
});
