<template>
  <div>
    <nav style="margin-bottom: 20px;">
      <router-link to="/">Home</router-link> |
      <router-link to="/movies">Movies</router-link> |
      <router-link to="/rent">Rent</router-link>
    </nav>
    <router-view />
  </div>
</template>
