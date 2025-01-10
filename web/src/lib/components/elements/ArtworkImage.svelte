<script lang="ts">
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let width: string | number | undefined = undefined;
  export let height: string | number | undefined = undefined;
  export let FullCover: boolean = false;
  export let lazyload: boolean = true;
  
  $: showArtwork = true;
</script>


<div style="height: {height}px;">
  {#if showArtwork}
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <img
      loading={lazyload ? "lazy" : "eager"}
      {src}
      {alt}
      {width}
      {height}
      on:click
      on:keydown
      on:mousedown
      on:mouseleave
      on:error={() => showArtwork = !showArtwork}
      class:full={FullCover}
    />
  {/if}
</div>


<style>
  div {
    aspect-ratio: 1/1;
    display: flex;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-s);
  }

  img {
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
    object-fit: scale-down;
    user-select: none;
    -webkit-user-drag: none;
  }

  .full {
    object-fit: cover;
  }
</style>
