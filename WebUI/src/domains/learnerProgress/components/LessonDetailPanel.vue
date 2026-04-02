<template>
  <VCard class="g-panel lesson-detail-panel">
    <div v-if="loading" class="lesson-detail-panel__state">
      <VProgressCircular indeterminate color="secondary" />
      <p>Loading lesson content…</p>
    </div>

    <div v-else-if="!lesson" class="lesson-detail-panel__state g-muted-text">
      Pick a lesson to inspect blocks and progress.
    </div>

    <template v-else>
      <header class="lesson-detail-panel__header">
        <div>
          <p class="g-kicker">Lesson Detail</p>
          <h2 class="lesson-detail-panel__title">{{ lesson.lesson.title }}</h2>
          <p class="g-muted-text">/{{ lesson.lesson.slug }}</p>
        </div>

        <div class="lesson-detail-panel__summary-grid">
          <span class="g-inline-chip">{{ lesson.progress_summary.seen_blocks }} seen</span>
          <span class="g-inline-chip">{{ lesson.progress_summary.completed_blocks }} completed</span>
          <span class="g-inline-chip">
            {{ lesson.progress_summary.completed ? "Lesson complete" : "Still in progress" }}
          </span>
        </div>
      </header>

      <div class="lesson-detail-panel__blocks">
        <VCard
          v-for="block in lesson.blocks"
          :key="block.id"
          class="lesson-detail-panel__block"
          rounded="xl"
          variant="outlined"
        >
          <div class="lesson-detail-panel__block-header">
            <div>
              <p class="g-kicker">Block {{ block.position }}</p>
              <h3 class="lesson-detail-panel__block-title">{{ blockTitle(block) }}</h3>
            </div>
            <span class="g-inline-chip">{{ block.user_progress ?? "not started" }}</span>
          </div>

          <p class="g-muted-text lesson-detail-panel__block-copy">
            {{ blockDescription(block) }}
          </p>

          <div class="lesson-detail-panel__block-actions">
            <VBtn
              color="secondary"
              variant="tonal"
              :loading="updatingBlockId === block.id"
              @click="$emit('mark', block.id, 'seen')"
            >
              Mark seen
            </VBtn>
            <VBtn
              color="primary"
              :loading="updatingBlockId === block.id"
              @click="$emit('mark', block.id, 'completed')"
            >
              Mark completed
            </VBtn>
          </div>
        </VCard>
      </div>
    </template>
  </VCard>
</template>

<script setup lang="ts">
import type { LessonBlock, LessonResponse, UserProgressStatus } from "@/types/api";

defineProps<{
  lesson: LessonResponse | null;
  loading: boolean;
  updatingBlockId: number | null;
}>();

defineEmits<{
  mark: [blockId: number, status: UserProgressStatus];
}>();

function blockTitle(block: LessonBlock): string {
  const heading = block.variant.data.heading;
  return typeof heading === "string" ? heading : `${block.type} block`;
}

function blockDescription(block: LessonBlock): string {
  const body = block.variant.data.body;
  return typeof body === "string"
    ? body
    : "This variant is ready for richer rendering once the real exercise data is wired in.";
}
</script>

<style scoped lang="scss">
.lesson-detail-panel {
  min-height: 32rem;
  padding: $spacing-lg;
}

.lesson-detail-panel__state {
  min-height: 24rem;
  display: grid;
  place-items: center;
  text-align: center;
}

.lesson-detail-panel__header {
  display: flex;
  justify-content: space-between;
  gap: $spacing-lg;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $theme-border;
}

.lesson-detail-panel__title {
  margin: 0;
}

.lesson-detail-panel__summary-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: end;
  gap: $spacing-sm;
  align-content: start;
}

.lesson-detail-panel__blocks {
  display: grid;
  gap: $spacing-md;
  padding-top: $spacing-lg;
}

.lesson-detail-panel__block {
  padding: $spacing-lg;
  border-color: $theme-border;
}

.lesson-detail-panel__block-header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: $spacing-md;
}

.lesson-detail-panel__block-title {
  margin: 0;
}

.lesson-detail-panel__block-copy {
  margin: $spacing-md 0;
}

.lesson-detail-panel__block-actions {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-sm;
}
</style>
