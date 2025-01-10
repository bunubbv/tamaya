<script lang="ts">
  import Dropdown from '$lib/components/elements/Dropdown.svelte';
  import DropdownItem from '$lib/components/elements/DropdownItem.svelte';
  import { handleLogout } from '$lib/tools';
  import { _ } from 'svelte-i18n'
</script>


<Dropdown dropdownOpenIcon='iconoir:user'>
  
  <DropdownItem icon="iconoir:settings">
    {$_('settings.user')}
  </DropdownItem>

  <DropdownItem icon="iconoir:wrench">
    {$_('settings.server')}
  </DropdownItem>

  <DropdownItem
    icon="iconoir:log-out"
    on:click={() => handleLogout(window.fetch)}
  >
    {$_('logout')}
  </DropdownItem>

</Dropdown>
