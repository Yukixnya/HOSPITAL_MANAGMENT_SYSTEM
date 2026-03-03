<script setup>
import { TrendingUp, TrendingDown } from 'lucide-vue-next';
defineProps(['title', 'value', 'trend', 'isUp', 'icon', 'iconBg', 'iconColor']);
</script>

<template>
  <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
    <div class="flex justify-between items-start mb-4">
      <div :class="[iconBg, 'p-2 rounded-lg']">
        <component :is="icon" :class="iconColor" :size="20" />
      </div>
      <div :class="['flex items-center gap-1 text-xs font-bold', isUp ? 'text-emerald-500' : 'text-red-500']">
        <component :is="isUp ? TrendingUp : TrendingDown" :size="14" />
        {{ trend }}
      </div>
    </div>
    <p class="text-slate-400 text-sm font-medium">{{ title }}</p>
    <h3 class="text-2xl font-bold text-slate-800 mt-1">{{ value }}</h3>
  </div>
</template>