<script lang="ts">
  import { getArtwork } from '$lib/tools';

  export let albumId: string;
  let imageUrl = getArtwork(albumId, 500);
</script>


<div
  class="album-wrap"
  style="background-image: url({imageUrl})"
/>


<style>
  .album-wrap {
    position: absolute;
    width: 100%;
    height: 50dvh;
    z-index: -1;
    background-size: cover;
    background-position-y: center;
    border-image: fill 0 linear-gradient(
      to top,
      hsl(0, 0%, 7%) 0%,
      hsla(0, 0%, 7.13%, 0.997) 8.6%,
      hsla(0, 0%, 7.49%, 0.99) 17.5%,
      hsla(0, 0%, 8.02%, 0.979) 26.5%,    
      hsla(0, 0%, 8.65%, 0.965) 35.6%,   
      hsla(0, 0%, 9.33%, 0.948) 44.6%,  
      hsla(0, 0%, 10.04%, 0.93) 53.3%,   
      hsla(0, 0%, 10.73%, 0.91) 61.7%,    
      hsla(0, 0%, 11.39%, 0.89) 69.6%,     
      hsla(0, 0%, 12.01%, 0.87) 76.9%,  
      hsla(0, 0%, 12.57%, 0.852) 83.4%, 
      hsla(0, 0%, 13.05%, 0.835) 89%,   
      hsla(0, 0%, 13.44%, 0.821) 93.6%, 
      hsla(0, 0%, 13.74%, 0.81) 97.1%, 
      hsla(0, 0%, 13.93%, 0.803) 99.2%, 
      hsla(0, 0%, 14%, 0.8) 100%
    );

    /* border-image: fill 0 linear-gradient(to bottom, hsla(0, 0%, 7%, 0.63) 0%, hsla(0, 0%, 6.99%, 0.635) 8.1%, hsla(0, 0%, 6.95%, 0.648) 15.5%, hsla(0, 0%, 6.9%, 0.668) 22.5%, hsla(0, 0%, 6.84%, 0.695) 29%, hsla(0, 0%, 6.75%, 0.726) 35.3%, hsla(0, 0%, 6.67%, 0.76) 41.2%, hsla(0, 0%, 6.57%, 0.797) 47.1%, hsla(0, 0%, 6.47%, 0.833) 52.9%, hsla(0, 0%, 6.37%, 0.87) 58.8%, hsla(0, 0%, 6.27%, 0.904) 64.7%, hsla(0, 0%, 6.19%, 0.935) 71%, hsla(0, 0%, 6.11%, 0.962) 77.5%, hsla(0, 0%, 6.05%, 0.982) 84.5%, hsla(0, 0%, 6.01%, 0.995) 91.9%, hsl(0, 0%, 6%) 100%); */
  }
</style>
