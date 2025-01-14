import type {
  AlbumsResponse,
  AlbumResponse,
  TracksResponse,
  TrackResponse,
  ArtistsResponse,
  ArtistResponse,
  PlaylistsResponse,
  PlaylistResponse,
} from "./interface";
import { apiFetch } from "./tools";


export async function postLogout(
  fetch: typeof window.fetch
): Promise<void> {
  
  try {
    const postLogout = await fetch(
      `http://localhost:2843/api/auth/logout`,
      {
        method: 'POST',
        credentials: 'include',
      }
    );

    if (!postLogout.ok) {
      throw new Error(postLogout.statusText);
    }

    window.location.href = '/signin';

  }

  catch (error) {
    console.error('Logout failed:', error);
    throw new Error('Failed to log out');
  }
}


export async function getTracks(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: TracksResponse;}> {

  try {
    const fetchTracks = await apiFetch(fetch,
      `http://localhost:2843/api/library/tracks?start=${start}&end=${end}`);

    if (!fetchTracks.ok) {
      throw new Error(fetchTracks.statusText);
    }

    const response: TracksResponse = await fetchTracks.json();

    return {
      response,
    };
  }
  
  catch (error) {
    return {
      response: {
        "tracks": [],
        "total": 0,
      },
    }
  }
};


export async function getTrack(
  fetch: typeof window.fetch,
  trackId: string,
): Promise<{response: TrackResponse;}> {
  
  try {
    const fetchTrack = await apiFetch(fetch,
      `http://localhost:2843/api/library/tracks/${trackId}`);

    if (!fetchTrack.ok) {
      throw new Error(fetchTrack.statusText);
    }

    const response: TrackResponse = await fetchTrack.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getAlbums(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: AlbumsResponse;}> {

  try {
    const fetchAlbums = await apiFetch(fetch,
      `http://localhost:2843/api/library/albums?start=${start}&end=${end}`);

    if (!fetchAlbums.ok) {
      throw new Error(fetchAlbums.statusText);
    }

    const response: AlbumsResponse = await fetchAlbums.json();

    return {
      response,
    };
  }

  catch (error) {
    return {
      response: {
        "albums": [],
        "total": 0,
      },
    }
  }
};


export async function getAlbum(
  fetch: typeof window.fetch,
  albumId: string,
): Promise<{response: AlbumResponse;}> {

  try {
    const fetchAlbum = await apiFetch(fetch,
      `http://localhost:2843/api/library/albums/${albumId}`);

    if (!fetchAlbum.ok) {
      throw new Error(fetchAlbum.statusText);
    }

    const response: AlbumResponse = await fetchAlbum.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getArtists(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: ArtistsResponse;}> {

  try {
    const fetchArtists = await apiFetch(fetch,
      `http://localhost:2843/api/library/artists?start=${start}&end=${end}`);

    if (!fetchArtists.ok) {
      throw new Error(fetchArtists.statusText);
    }

    const response: ArtistsResponse = await fetchArtists.json();

    return {
      response,
    };
  }

  catch (error) {
    return {
      response: {
        "artists": [],
        "total": 0,
      },
    }
  }
};


export async function getArtist(
  fetch: typeof window.fetch,
  artistId: string,
): Promise<{response: ArtistResponse;}> {

  try {
    const fetchArtist = await apiFetch(fetch,
      `http://localhost:2843/api/library/artists/${artistId}`);

    if (!fetchArtist.ok) {
      throw new Error(fetchArtist.statusText);
    }

    const response: ArtistResponse = await fetchArtist.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getPlaylists(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: PlaylistsResponse;}> {

  try {
    const fetchArtists = await apiFetch(fetch,
      `http://localhost:2843/api/playlists?start=${start}&end=${end}`);

    if (!fetchArtists.ok) {
      throw new Error(fetchArtists.statusText);
    }

    const response: PlaylistsResponse = await fetchArtists.json();

    return {
      response,
    };
  }

  catch (error) {
    return {
      response: {
        "playlists": [],
        "total": 0,
      },
    }
  }
};


export async function getPlaylist(
  fetch: typeof window.fetch,
  playListId: string,
): Promise<{response: PlaylistResponse;}> {

  try {
    const fetchPlaylist = await apiFetch(fetch,
      `http://localhost:2843/api/playlists/${playListId}`);

    if (!fetchPlaylist.ok) {
      throw new Error(fetchPlaylist.statusText);
    }

    const response: PlaylistResponse = await fetchPlaylist.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};
