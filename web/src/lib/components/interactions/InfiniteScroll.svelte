<script lang="ts">
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  
  export let threshold: number = 2000;
  const dispatch = createEventDispatcher();
  let contentContainer: HTMLElement;

  function onScroll() {
    const { scrollTop, scrollHeight, clientHeight } = contentContainer;
    if (scrollHeight - scrollTop - clientHeight <= threshold) {
      dispatch('loadMore');
    }
  }

  onMount(() => {
    contentContainer = document.querySelector('#wrap');
    if (contentContainer) {
      contentContainer.addEventListener('scroll', onScroll);
    }

    return () => {
      if (contentContainer) {
        contentContainer.removeEventListener('scroll', onScroll);
      }
    };
  });
</script>

<slot />
