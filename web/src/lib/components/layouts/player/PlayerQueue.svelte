<script lang="ts">
  import ArtworkImage from "$lib/components/elements/ArtworkImage.svelte";
  import PlayerService from "$lib/stores/stores";
  import Button from "$lib/components/elements/Button.svelte";
  import { convertDateTime, getArtistLink, getArtwork } from "$lib/tools";
  import { isQueueOpen } from "$lib/stores/layout";
  import { fly, fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { _ } from "svelte-i18n";
  import { onMount, onDestroy } from "svelte";

  $: lists = $PlayerService;
  let playerQueueElement;

  export const handlePlayerQueueClick = () => {
    $isQueueOpen = !$isQueueOpen;
  };

  const handleClickOutside = (event) => {
    if (playerQueueElement && !playerQueueElement.contains(event.target)) {
      $isQueueOpen = false;
    }
  };

  onMount(() => {
    document.addEventListener("click", handleClickOutside);
  });

  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
</script>

{#if $isQueueOpen}
  <div bind:this={playerQueueElement} class="player-queue"
  transition:fly={
    { 
      delay: 10,
      duration: 500,
      x: document.querySelector('.player-queue').clientWidth + 20,
      opacity: 1,
      easing: cubicOut
    }
  }>
    <!-- <span class="title">{$_('player.queue')}</span> -->
    {#each lists.lists as trk, index}
      <div in:fade={{ duration: 100 }} out:fade={{ duration: 100 }} class="track">
        <ArtworkImage
          src={trk.album === ''
            ? getArtwork(trk.track_id, 128)
            : trk.album_id && getArtwork(trk.album_id, 128)
          }
          width=45
          height=45
          alt={$_('player.front_cover')}
          FullCover
        />

        <div class="left">
          <!-- svelte-ignore a11y-missing-attribute -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <a class="text bold" on:click={() =>
            PlayerService.setTrack(index)
          }>
              {trk.title}
          </a>
          <span class="text-sub">
            <a href="{getArtistLink(trk.artist_id)}">
              {trk.artist}
            </a>
          </span>
        </div>

        <div class="right">
          <span class="text-sub">
            {convertDateTime(trk.duration)}
          </span>

          <Button
            button='custom'
            width='21px'
            height='32px'
            iconSize='21'
            iconName='iconoir:xmark'
            on:click={() => PlayerService.delTrack(index)}
          />
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .player-queue {
    z-index: 0;
    display: flex;
    position: fixed;
    top: var(--space-s);
    right: var(--space-s);
    flex-direction: column;
    flex-shrink: 0;
    width: 340px;
    height: calc(100% - 96px - calc(var(--space-s)* 2));
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    background-color: var(--dark-queue);
    border-radius: var(--radius-m);
    gap: 18px;
    overflow-y: scroll;
    padding: var(--space-s);
    backdrop-filter: blur(64px);
  }

  .track {
    display: flex;
    flex-direction: row;
    gap: var(--space-s);
  }

  .left {
    display: inline-flex;
    flex-direction: column;
    justify-content: space-around;
    white-space: nowrap;
    overflow: hidden;
  }

  .right {
    display: inline-flex;
    margin-left: auto;
    align-items: center;
    gap: var(--space-xs);
  }

  a {
    display: block;
    width: auto;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
