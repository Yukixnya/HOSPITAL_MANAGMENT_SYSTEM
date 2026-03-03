<template>
  <div class="flex min-h-screen bg-slate-50">
    
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 pl-64">
      <Navabr />
        <router-view />
      </div>
  </div>
</template>

<script setup>
import Navabr from '../components/Navabr.vue';
import Sidebar from '../components/SideNavbar.vue';
</script>