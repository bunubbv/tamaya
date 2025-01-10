<script lang="ts">
  import type { Tracks } from "$lib/interface";
  import PlayerService from "$lib/stores/stores";
  import Button from "./elements/Button.svelte";
  import { _ } from 'svelte-i18n'

  export let tracks: Tracks[];
</script>


<div class="controls-bar">
  <div>
    <Button
      button='square'
      width='150px'
      height='50px'
      title={$_('controls.play')}
      iconName='iconoir:play-solid'
      on:click={() =>
        PlayerService.addTrack(
          tracks.map(track => ({
            album: track.album,
            album_id: track.album_id,
            artist: track.artist,
            artist_id: track.artist_id,
            duration: track.duration,
            title: track.title,
            track_id: track.track_id,
          }))
        , true)
      }
    >
      {$_('controls.play')}
    </Button>

    <Button
      button='square'
      width='150px'
      height='50px'
      title={$_('controls.shuffle')}
      iconName='iconoir:shuffle'
    >
      {$_('controls.shuffle')}
    </Button>
  </div>
</div>


<style>
  .controls-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  .controls-bar > div {
    display: flex;
    gap: var(--space-s);
  }
</style>
