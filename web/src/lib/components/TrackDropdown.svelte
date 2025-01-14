<script lang="ts">
  import type { AlbumTrack, Tracks } from "$lib/interface";
  import Dropdown from '$lib/components/elements/Dropdown.svelte';
  import DropdownItem from '$lib/components/elements/DropdownItem.svelte';
  import { getArtistLink, handleLogout } from '$lib/tools';
  import { _ } from 'svelte-i18n'
  import PlayerService from "$lib/stores/stores";

  export let track: Tracks;
</script>


<Dropdown
  dropdownStyle='custom'
  dropdownOpenIcon='iconoir:more-horiz'
>

  <DropdownItem
    icon="iconoir:play"
    on:click={() =>
      PlayerService.addTrack(
        [{
          album: track.album,
          album_id: track.album_id,
          artist: track.artist,
          artist_id: track.artist_id,
          duration: track.duration,
          title: track.title,
          track_id: track.track_id,
        }]
      , true)
    }
  >
    재생
  </DropdownItem>

  <DropdownItem
    icon="iconoir:playlist-play"
    on:click={() =>
      PlayerService.addTrack(
        [{
          album: track.album,
          album_id: track.album_id,
          artist: track.artist,
          artist_id: track.artist_id,
          duration: track.duration,
          title: track.title,
          track_id: track.track_id,
        }]
      , false, PlayerService.getState.index + 1)
    }
  >
    <!-- 현재 재생 중인 트랙이 꼭 0번째 순서일까?????????? -->
    다음에 재생
  </DropdownItem>

  <DropdownItem
    icon="iconoir:playlist-plus"
    on:click={() =>
      PlayerService.addTrack(
        [{
          album: track.album,
          album_id: track.album_id,
          artist: track.artist,
          artist_id: track.artist_id,
          duration: track.duration,
          title: track.title,
          track_id: track.track_id,
        }]
      )
    }
  >
    재생목록에 추가
  </DropdownItem>

  <DropdownItem
    icon="iconoir:user"
    href={getArtistLink(track.artist_id)}
  >
    아티스트 페이지로
  </DropdownItem>

  <DropdownItem
    icon="iconoir:download"
    href='http://localhost:2843/api/library/download/{track.track_id}'
  >
    다운로드
  </DropdownItem>

  <DropdownItem
    icon="iconoir:info-circle"
    on:click={() => handleLogout(window.fetch)}
  >
    세부 정보
  </DropdownItem>

</Dropdown>
