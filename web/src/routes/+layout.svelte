<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import { page } from '$app/stores';
  import { afterNavigate } from '$app/navigation';
  import PlayerService from '$lib/stores/stores';

  let previousPathname: string | null = null;

  afterNavigate(() => {
    const currentPathname = $page.url.pathname;
    
    if (previousPathname == null || currentPathname !== previousPathname) {
      document.getElementById("contents")?.scrollIntoView({
        block: "start",
        inline: "nearest",
      });
    }

    previousPathname = currentPathname;
  });

  onDestroy(() => {
    PlayerService.destroy();
  })
</script>


<div id="app">
  <slot />
</div>


<style>
  #app {
    width: 100%;
    display: flex;
    height: 100dvh;
  }
</style>
