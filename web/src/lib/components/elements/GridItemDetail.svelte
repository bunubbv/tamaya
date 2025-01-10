<script lang="ts">
  export let center: boolean = false;
  export let title: string;
  export let titleHref: any = undefined;
  export let sub: string | undefined = undefined;
  export let subHref: any = undefined;
</script>


<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class:center={center}>
  <a href={titleHref} class="text bold">{title}</a>
  {#if sub}
    {#if subHref}
      <a href={subHref} class="text-sub">
        {sub}
      </a>
    {:else}
      <span class="text-sub">{sub}</span>
    {/if}
  {/if}
</div>


<style>
  div {
    padding-top: var(--space-s);
  }

  a {
    width: auto;
    display: block;
    text-overflow: ellipsis;
    overflow: hidden;
    line-height: 150%;
  }

  .center {
    text-align: center;
  }
</style>