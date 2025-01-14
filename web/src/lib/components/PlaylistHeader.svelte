<script lang="ts">
  import type { PlaylistTrack } from "$lib/interface";
  import ArtworkImage from "./elements/ArtworkImage.svelte";
  import ControlsBar from "./ControlsBar.svelte";
  import { getArtwork } from "$lib/tools";
  import { _ } from "svelte-i18n";
  
  export let playlist_id: string;
  export let playlist_title: string;
  export let playlist_username: string;
  export let tracks: PlaylistTrack[] | undefined = undefined;

  $: artwork = getArtwork(playlist_id, 500);
</script>


<div class="playlist-header">
  <ArtworkImage
    src={artwork}
    alt={playlist_title}
    width={270}
    height={270}
    lazyload={false}
  />

  <div class="playlist-details">
    <div>
      <span class="title">
        {playlist_title}
      </span>

      <span class="artist">
        {playlist_username}
      </span>
    </div>

    {#if tracks}
      <ControlsBar {tracks} />
    {/if}
  </div>
</div>


<style>
  .playlist-header {
    display: flex;
    width: 100%;
    gap: var(--space-l);
    flex-direction: row;
    margin-bottom: var(--space-l);
  }

  .playlist-details {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
  }

  .playlist-details > div {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: flex-end;
  }

  .title {
    font-size: clamp(1rem, 3vw, 2rem);
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .artist {
    color: var(--dark-text-sub);
    font-size: clamp(1rem, 3vw, 2rem);
  }
</style>
