<script lang="ts">
  import { getArtwork } from "$lib/tools";
  import ArtworkImage from "./ArtworkImage.svelte";

  export let href: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
</script>


<div class="grid-item">
  {#if src}
    <a
      data-sveltekit-preload-data tabindex="-1" on:click {href}>
      <ArtworkImage src={getArtwork(src, 300)} {alt}/>
    </a>
    <slot />

  {:else}
    <!-- svelte-ignore a11y-missing-content -->
    <a data-sveltekit-preload-data tabindex="-1" on:click {href} />
    <slot />

  {/if}
</div>


<style>
  .grid-item {
    white-space: nowrap;
    margin-bottom: var(--space-m);
  }

  a {
    user-select: none;
    -webkit-user-drag: none;
  }
</style>
