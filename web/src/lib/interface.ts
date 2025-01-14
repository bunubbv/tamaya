export interface Tracks {
  album: string;
  album_id: string;
  artist: string;
  artist_id: string;
  duration: number;
  title: string;
  track_id: string;
};


export interface TracksResponse {
  tracks: Tracks[];
  total: number;
};


export interface Track {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  artist: string;
  artist_id: string;
  barcode?: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  compilation: boolean;
  comment?: string;
  composer?: string;
  content_type: string;
  copyright?: string;
  created_at?: string;
  date?: string;
  director?: string;
  directory: string;
  duration: number;
  disc_number: number;
  disc_total: number;
  filepath: string;
  filesize: number;
  genre?: string;
  isrc?: string;
  label?: string;
  lyrics?: string;
  samplerate: number;
  title: string;
  track_id: string;
  track_number: number;
  track_total: number;
  updated_at: string;
  year?: number;
};


export interface TrackResponse extends Track {};


export interface Albums {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  year?: number;
};


export interface AlbumsResponse {
  albums: Albums[]
  total: number;
};


export interface Album {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  disc_total: number;
  duration_total: number;
  filesize_total: number;
  year?: number;
};


export interface AlbumTrack {
  artist: string;
  artist_id: string;
  comment?: string;
  duration: number;
  title: string;
  track_id: string;
  track_number: number;
};


export interface AlbumResponse extends Album {
  tracks: AlbumTrack[];
};


export interface Artists {
  artist: string;
  artist_id: string;
  album_total: number;
  track_total: number;
  duration_total: number;
  filesize_total: number;
};


export interface ArtistsResponse {
  artists: Artists[];
  total: number;
};


export interface Artist {
  artist: string;
  artist_id: string;
  album_total: number;
  track_total: number;
  duration_total: number;
  filesize_total: number;
};


export interface ArtistAlbum {
  album: string;
  album_id: string;
  albumartist_id: string;
  year?: number;
};


export interface ArtistResponse extends Artist {
  albums: ArtistAlbum[];
};


export interface PlayerState {
  index: number;
  lists: Tracks[];
  isLoaded: boolean;
  isPlaying: boolean;
  currentTime: number;
  volumeRange: number;
  duration: number;
  volume: number;
  mute: boolean;
  loop: number;
};


export interface PlayerStore extends PlayerState, Tracks {
  artwork?: string;
};


export interface Playlist {
  playlist_id: string;
  playlist_title: string;
  playlist_user_id: string;
  playlist_username: string;
  created_at: string;
  updated_at: string;
};


export interface PlaylistData {
  playlist_id: string;
  track_id: string;
  added_at: string;
  order: number;
};


export interface PlaylistTrack {
  album: string;
  album_id: string;
  artist: string;
  artist_id: string;
  duration: number;
  title: string;
  track_id: string;
};


export interface PlaylistsResponse {
  playlists: Playlist[];
  total: number;
};


export interface PlaylistResponse extends Playlist {
  tracks: PlaylistTrack[];
};
