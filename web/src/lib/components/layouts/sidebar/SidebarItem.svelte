<script lang="ts">
  import Icon from '@iconify/svelte';
  export let icon: string | undefined = undefined;
  export let href: string;
</script>

<li>
  <a {href}>
    {#if icon}
      <span>
        <Icon {icon} width="24" height="24" />
      </span>
    {/if}

    <slot />
  </a>
</li>

<style>
  li {
    list-style: none;
    padding: 0 12px;
    border-radius: var(--radius-m);
  }

  a {
    width: 100%;
    display: flex;
    font-size: 15px;
    padding: 6px 12px;
    align-items: center;
    gap: var(--space-xs);
    border-radius: var(--radius-m);
    text-decoration: none;
    min-height: 50px;
    user-select: none;
    -webkit-user-drag: none;
  }

  a:hover {
    background-color: var(--black-4);
  }

  a:hover,
  a:focus,
  a:active {
    outline: none;
  }

  span {
    min-height: 36px;
    display: flex;
    font-size: 21px;
    color: var(--dark-text-sub);
    align-items: center;
    justify-content: center;
    margin-left: 2px;
  }

  /* li {
    display: flex;
    margin-bottom: var(--space-s);
    align-items: center;
  }

  a {
    display: flex;
    align-items: center;
    min-height: 36px;
    width: 100%;
  }





  span {
    width: 36px;
    min-height: 36px;
    display: flex;
    color: var(--dark-text-sub);
    align-items: center;
    justify-content: center;
  } */
</style>
