<script lang="ts">
  import type { Tracks } from "$lib/interface";
  import ArtworkImage from "./elements/ArtworkImage.svelte";
  import ControlsBar from "./ControlsBar.svelte";
  import { getArtistLink, getArtwork } from "$lib/tools";
  import { _ } from "svelte-i18n";
  export let album: string;
  export let albumId: string;
  export let albumArtist: string;
  export let albumArtistId: string;
  export let tracks: Tracks[] | undefined = undefined;

  $: artwork = getArtwork(albumId, 500);
</script>


<div class="album-header">
  <ArtworkImage
    src={artwork}
    alt={album}
    width={270}
    height={270}
    lazyload={false}
  />

  <div class="album-details">
    <div>
      <span class="title">
        {album ? album : $_('unknown_album')}
      </span>

      {#if albumArtist}
        <a href={getArtistLink(albumArtistId)}>
          <span class="artist">
            {albumArtist}
          </span>
        </a>
      {/if}
    </div>

    {#if tracks}
      <ControlsBar {tracks} />
    {/if}
  </div>
</div>


<style>
  .album-header {
    display: flex;
    width: 100%;
    gap: var(--space-l);
    flex-direction: row;
    margin-bottom: var(--space-l);
  }

  .album-details {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
  }

  .album-details > div {
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
