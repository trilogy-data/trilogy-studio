<template>
    <div class="glowing-dot" ></div>
  </template>
  
  <style scoped>
  .glowing-dot {
    width: 5px;
    height: 5px;
    border-radius: 25%;
    background-color: #00ff00; /* Green color */
    box-shadow: 0 0 2px rgba(0, 255, 0, 0.8);
    animation: glowAnimation 1s infinite alternate;
  }
  
  @keyframes glowAnimation {
    0% {
      box-shadow: 0 0 2px rgba(0, 255, 0, 0.8);
    }
    100% {
      box-shadow: 0 0 5px rgba(0, 255, 0, 0.6);
    }
  }
  </style>