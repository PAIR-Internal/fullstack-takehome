<template>
  <BasePageShell
    title="Learner Progress Slice"
    summary="A production-shaped starter for the PAIR take-home: typed API calls, a small Pinia store, and a learner workspace that is already wired for lesson and progress flows."
  >
    <VAlert
      v-if="store.errorMessage"
      type="error"
      variant="tonal"
      class="learner-workspace__alert"
      closable
      @click:close="store.errorMessage = null"
    >
      {{ store.errorMessage }}
    </VAlert>

    <div class="learner-workspace__layout">
      <LessonSidebar
        :lessons="store.lessons"
        :loading="store.loadingLessons"
        :selected-lesson-id="store.selectedLessonId"
        @refresh="store.loadLessons"
        @select="store.loadLesson"
      />

      <LessonDetailPanel
        :lesson="store.selectedLesson"
        :loading="store.loadingLesson"
        :updating-block-id="store.updatingBlockId"
        @mark="handleMark"
      />
    </div>
  </BasePageShell>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import BasePageShell from "@/components/common/BasePageShell.vue";
import LessonDetailPanel from "@/domains/learnerProgress/components/LessonDetailPanel.vue";
import LessonSidebar from "@/domains/learnerProgress/components/LessonSidebar.vue";
import { useLessonStore } from "@/stores/lessonStore";
import type { UserProgressStatus } from "@/types/api";

const store = useLessonStore();

onMounted(async () => {
  await store.loadLessons();
});

function handleMark(blockId: number, status: UserProgressStatus): void {
  if (!store.selectedLessonId) {
    return;
  }

  void store.markBlock(store.selectedLessonId, blockId, status);
}
</script>

<style scoped lang="scss">
.learner-workspace__alert {
  margin-bottom: $spacing-lg;
}

.learner-workspace__layout {
  display: grid;
  gap: $spacing-lg;
  grid-template-columns: minmax(18rem, 24rem) minmax(0, 1fr);
}

@media (max-width: 900px) {
  .learner-workspace__layout {
    grid-template-columns: 1fr;
  }
}
</style>
