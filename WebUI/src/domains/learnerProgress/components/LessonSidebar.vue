<template>
  <VCard class="g-panel lesson-sidebar">
    <div class="lesson-sidebar__header">
      <div>
        <p class="g-kicker">Lessons</p>
        <h2 class="lesson-sidebar__title">Available slices</h2>
      </div>
      <VBtn variant="text" icon="mdi-refresh" :loading="loading" @click="$emit('refresh')" />
    </div>

    <VProgressLinear v-if="loading" indeterminate color="secondary" class="lesson-sidebar__progress" />

    <div v-if="!loading && lessons.length === 0" class="lesson-sidebar__empty g-muted-text">
      No lessons are available for this learner yet.
    </div>

    <VList v-else lines="two" class="lesson-sidebar__list">
      <VListItem
        v-for="lesson in lessons"
        :key="lesson.id"
        :active="lesson.id === selectedLessonId"
        rounded="xl"
        @click="$emit('select', lesson.id)"
      >
        <template #title>
          <div class="lesson-sidebar__item-title">{{ lesson.title }}</div>
        </template>
        <template #subtitle>
          <div class="lesson-sidebar__item-meta">
            <span class="g-inline-chip">{{ lesson.status.replace('_', ' ') }}</span>
            <span>{{ lesson.progress_summary.completed_blocks }}/{{ lesson.progress_summary.total_blocks }} completed</span>
          </div>
        </template>
      </VListItem>
    </VList>
  </VCard>
</template>

<script setup lang="ts">
import type { LessonListItem } from "@/types/api";

defineProps<{
  lessons: LessonListItem[];
  loading: boolean;
  selectedLessonId: number | null;
}>();

defineEmits<{
  refresh: [];
  select: [lessonId: number];
}>();
</script>

<style scoped lang="scss">
.lesson-sidebar {
  padding: $spacing-lg;
}

.lesson-sidebar__header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: $spacing-md;
}

.lesson-sidebar__title {
  margin: 0;
}

.lesson-sidebar__progress {
  margin: $spacing-md 0;
}

.lesson-sidebar__list {
  padding: 0;
  background: transparent;
}

.lesson-sidebar__item-title {
  font-weight: 700;
}

.lesson-sidebar__item-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: $spacing-sm;
  margin-top: $spacing-xs;
}

.lesson-sidebar__empty {
  padding-top: $spacing-lg;
}
</style>
