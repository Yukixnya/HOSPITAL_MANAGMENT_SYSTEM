<script setup>
import { Analytics } from '@vercel/analytics/vue';
</script>
<template>
  <Analytics />
  <Suspense fallback="Loading...">
    <router-view />
  </Suspense>
</template>
