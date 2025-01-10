<script lang="ts">
  import SidebarList from './SidebarList.svelte';
  import SidebarItem from './SidebarItem.svelte';
  import { _ } from 'svelte-i18n';
  import { getPlaylists } from '../../../requests';

  let playlists = [];

  async function fetchPlaylists() {
    try {
        const { response } = await getPlaylists(window.fetch, 1, 40);
        playlists = response.playlists;
    }
    catch (error) {
      console.error('Failed to fetch playlists:', error);
      playlists = [];
    }
  }
  
  fetchPlaylists();
</script>

<div>
  <SidebarList>
    <SidebarItem href='/'>
      {$_('sidebar.home')}
    </SidebarItem>

    <SidebarItem href='/'>
      {$_('sidebar.search')}
    </SidebarItem>

    <SidebarItem href='/'>
      {$_('sidebar.my_mix')}
    </SidebarItem>
  </SidebarList>

  <SidebarList name={$_('sidebar.library')}>
    <SidebarItem href='/playlists' icon='iconoir:playlist'>
      {$_('sidebar.library.playlists')}
    </SidebarItem>

    <SidebarItem href='/recents' icon='iconoir:clock-rotate-right'>
      {$_('sidebar.library.recent_played')}
    </SidebarItem>

    <SidebarItem href='/artists' icon='iconoir:microphone'>
      {$_('sidebar.library.artists')}
    </SidebarItem>

    <SidebarItem href='/albums' icon='iconoir:compact-disc'>
      {$_('sidebar.library.albums')}
    </SidebarItem>
    
    <SidebarItem href='/tracks' icon='iconoir:music-double-note'>
      {$_('sidebar.library.tracks')}
    </SidebarItem>
  </SidebarList>

  <SidebarList name={$_('sidebar.playlists')}>
    <div class="sidebar-playlist">
      <SidebarItem href='' icon='iconoir:plus-circle'>
        {$_('sidebar.playlists.create')}
      </SidebarItem>

      {#if playlists.length > 0}
        {#each playlists as playlist}
          <SidebarItem href={`/playlists/${playlist.playlist_id}`} icon='iconoir:music-note'>
            {playlist.playlist_name}
          </SidebarItem>
        {/each}
      {/if}
    </div>
  </SidebarList>
</div>

<style>
  div {
    z-index: 0;
    width: 240px;
    flex-shrink: 0;
    background-color: var(--dark-sidebar);
    border-right: 1px solid var(--dark-border);
    padding: var(--space-m) 0;
  }

  .sidebar-playlist {
    position: fixed;
    height: calc(100dvh - 530px - 100px);
    bottom: 96px;
    width: 240px;
    overflow: scroll;
    padding: 0;
    padding-bottom: 21px;
  }
</style>
