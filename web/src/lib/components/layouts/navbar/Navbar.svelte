<script lang="ts">
  import TextBox from '$lib/components/elements/Textbox.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n'
  import UserDropdown from '$lib/components/UserDropdown.svelte';
</script>

<nav>
  <div>
    <Button
      button='round'
      iconName='iconoir:nav-arrow-left'
      on:click={() => history.back()}
    />
    <Button
      button='round'
      iconName='iconoir:nav-arrow-right'
      on:click={() => history.forward()}
    />
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder={$_('navbar.search')}
    />
    <Button button='round' iconName='iconoir:refresh' />

    <UserDropdown />
  </div>
</nav>

<style>
  nav {
    top: 0;
    display: flex;
    position: sticky;
    justify-content: space-between;
    padding: 27px 0;
  }

  div {
    display: flex;
    gap: 12px;
  }
</style>
