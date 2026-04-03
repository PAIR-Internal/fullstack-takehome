<template>
  <section class="g-page-shell">
    <div class="base-page-shell__hero">
      <p class="g-kicker">PAIR Learner Progress</p>
      <h1 class="base-page-shell__title">{{ title }}</h1>
      <p class="base-page-shell__summary g-muted-text">
        {{ summary }}
      </p>
    </div>

    <slot />
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  summary: string;
}>();
</script>

<style scoped lang="scss">
.base-page-shell__hero {
  max-width: 56rem;
  margin-bottom: $spacing-xl;
}

.base-page-shell__title {
  margin: 0;
  font-size: clamp(2.25rem, 5vw, 4rem);
  line-height: 0.95;
}

.base-page-shell__summary {
  max-width: 40rem;
  margin-top: $spacing-md;
  font-size: 1.05rem;
}
</style>
