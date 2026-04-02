<template>
  <VApp>
    <VMain>
      <RouterView />
    </VMain>
  </VApp>
</template>

<style lang="scss">
body {
  margin: 0;
  background: $theme-background;
  color: $theme-text;
  font-family: "Aeonik", "Montserrat", sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
