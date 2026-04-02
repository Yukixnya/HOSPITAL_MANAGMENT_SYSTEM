import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../store/userStore.js";
import landing from "../pages/landing.vue";

const routes = [
  { path: "/", component: landing },

  // Auth Pages (Consolidated)
  {
    path: "/auth",
    component: () => import("../layout/AuthLayout.vue"),
    children: [
      { path: "login", component: () => import("../pages/auth/Login.vue") },
      { path: "register", component: () => import("../pages/auth/Register.vue") },
      { path: "", redirect: "/auth/login" },
    ],
  },

  // Admin Pages
  {
    path: "/admin",
    component: () => import("../layout/AdminLayout.vue"),
    meta: { requiresAuth: true, role: "admin" },
    children: [
      { path: "", component: () => import("../pages/admin/Dashboard.vue") },
      { path: "doctors", component: () => import("../pages/admin/Doctor.vue") },
      { path: "patients", component: () => import("../pages/admin/Patient.vue") },
      { path: "appointments", component: () => import("../pages/admin/Appointments.vue") },
    ],
  },

  // Doctor Pages
  {
    path: "/doctor",
    component: () => import("../layout/DoctorLayout.vue"),
    meta: { requiresAuth: true, role: "doctor" },
    children: [
      { path: "", component: () => import("../pages/doctor/Dashboard.vue") },
      { path: "patients", component: () => import("../pages/doctor/Patient.vue") },
      { path: "patients/:id", component: () => import("../pages/doctor/PatientDetails.vue") },
      { path: "appointments", component: () => import("../pages/doctor/Appointments.vue") },
      { path: "appointments/:id", component: () => import("../pages/doctor/PatientAppointmentReport.vue") },
    ],
  },

  // Patient Pages
  {
    path: "/patient",
    component: () => import("../layout/PatientLayout.vue"),
    meta: { requiresAuth: true, role: "patient" },
    children: [
      { path: "", component: () => import("../pages/patient/dashboard.vue") },
      { path: "my-appointments", component: () => import("../pages/patient/MyAppointments.vue") },
      { path: "my-appointments/past/:id", component: () => import("../pages/patient/PastAppointmentDetails.vue") },
      { path: "doctors", component: () => import("../pages/patient/DoctorList.vue") },
      { path: "doctors/:id", component: () => import("../pages/patient/DoctorProfile.vue") },
      { path: "medical-history", component: () => import("../pages/patient/MedicalHistory.vue") },
      { path: "profile", component: () => import("../pages/patient/Profile.vue") }
    ],
  },

  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Navigation Guard
 */
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  if (!to.meta.requiresAuth) {
    if (userStore.isLoggedIn && to.path.startsWith('/auth')) {
      return next(`/${userStore.user.role}`); 
    }
    return next();
  }

  if (!userStore.isLoggedIn) {
    if (to.path !== '/auth/login') {
      return next('/auth/login');
    }
    return next();
  }

  next();
});
export default router;