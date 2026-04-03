import { defineStore } from "pinia";

import { fetchLesson, fetchLessons, updateBlockProgress } from "@/services/api";
import type { LessonListItem, LessonResponse, UserProgressStatus } from "@/types/api";

interface LessonState {
  lessons: LessonListItem[];
  selectedLessonId: number | null;
  selectedLesson: LessonResponse | null;
  loadingLessons: boolean;
  loadingLesson: boolean;
  updatingBlockId: number | null;
  errorMessage: string | null;
}

export const useLessonStore = defineStore("lessonStore", {
  state: (): LessonState => ({
    lessons: [],
    selectedLessonId: null,
    selectedLesson: null,
    loadingLessons: false,
    loadingLesson: false,
    updatingBlockId: null,
    errorMessage: null,
  }),
  getters: {
    selectedLessonTitle: (state) => state.selectedLesson?.lesson.title ?? "Select a lesson",
  },
  actions: {
    async loadLessons() {
      this.loadingLessons = true;
      this.errorMessage = null;

      try {
        const response = await fetchLessons();
        this.lessons = response.lessons;

        if (!this.selectedLessonId && response.lessons.length > 0) {
          this.selectedLessonId = response.lessons[0].id;
          await this.loadLesson(response.lessons[0].id);
        }
      } catch (error) {
        this.errorMessage = error instanceof Error ? error.message : "Unable to load lessons.";
      } finally {
        this.loadingLessons = false;
      }
    },
    async loadLesson(lessonId: number) {
      this.loadingLesson = true;
      this.errorMessage = null;
      this.selectedLessonId = lessonId;

      try {
        this.selectedLesson = await fetchLesson(lessonId);
      } catch (error) {
        this.errorMessage = error instanceof Error ? error.message : "Unable to load lesson.";
      } finally {
        this.loadingLesson = false;
      }
    },
    async markBlock(lessonId: number, blockId: number, status: UserProgressStatus) {
      this.updatingBlockId = blockId;
      this.errorMessage = null;

      try {
        await updateBlockProgress(lessonId, {
          block_id: blockId,
          status,
        });

        await Promise.all([this.loadLessons(), this.loadLesson(lessonId)]);
      } catch (error) {
        this.errorMessage = error instanceof Error ? error.message : "Unable to update progress.";
      } finally {
        this.updatingBlockId = null;
      }
    },
  },
});
