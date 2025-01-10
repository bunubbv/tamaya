<script lang="ts">
  import Button from "./Button.svelte";
  import { onMount, onDestroy } from "svelte";
  import { fade } from "svelte/transition";

  let isDropdownOpen = false;
  export let dropdownStyle: string = 'round';
  export let dropdownWidth: string = '';
  export let dropdownOpenIcon: string | undefined = undefined;
  export let dropdownCloseIcon: string | undefined = undefined;

  let dropdownElement: HTMLElement | null = null;
  let buttonElement: HTMLElement | null = null;
  let dropdownPosition = { top: 0, left: 0 };
  let wrapElement: HTMLElement | null = null;

  if (dropdownCloseIcon === undefined && dropdownOpenIcon) {
    dropdownCloseIcon = dropdownOpenIcon;
  }

  const calculateDropdownPosition = () => {
    if (!buttonElement || !dropdownElement) return;

    const buttonRect = buttonElement.getBoundingClientRect();
    const dropdownRect = dropdownElement.getBoundingClientRect();

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let left = buttonRect.left + window.scrollX;
    let top = buttonRect.bottom + window.scrollY;

    // Adjust `left` to keep the dropdown within the viewport
    if (left + dropdownRect.width > viewportWidth) {
      left = viewportWidth - dropdownRect.width - 10; // Add padding from the edge
    }
    if (left < 0) {
      left = 10; // Add padding from the left edge
    }

    // Adjust `top` to keep the dropdown within the viewport
    if (top + dropdownRect.height > viewportHeight + window.scrollY) {
      top = buttonRect.top + window.scrollY - dropdownRect.height - 10; // Place above button
    }

    dropdownPosition = { top, left };
  };

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;

    if (isDropdownOpen) {
      calculateDropdownPosition();

      // Prevent background scrolling when dropdown is open
      if (wrapElement) {
        wrapElement.style.overflow = 'hidden';
      }
    } else {
      // Allow background scrolling when dropdown is closed
      if (wrapElement) {
        wrapElement.style.overflow = '';
      }
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownElement && !dropdownElement.contains(event.target as Node) &&
      buttonElement && !buttonElement.contains(event.target as Node)
    ) {
      closeDropdown();
    }
  };

  const closeDropdown = () => {
    isDropdownOpen = false;

    if (wrapElement) {
      wrapElement.style.overflow = '';
    }
  };

  onMount(() => {
    wrapElement = document.getElementById("wrap");
    document.addEventListener("click", handleClickOutside);
  });

  onDestroy(() => {
    closeDropdown(); // Ensure cleanup
    document.removeEventListener("click", handleClickOutside);
  });
</script>

<div bind:this={buttonElement} class="dropdown">
  <Button
    button={dropdownStyle}
    iconName={isDropdownOpen ? dropdownCloseIcon : dropdownOpenIcon}
    on:click={handleDropdownClick}
    aria-expanded={isDropdownOpen}
    aria-controls="dropdown-menu"
  />
</div>

{#if isDropdownOpen}
  <div
    bind:this={dropdownElement}
    id="dropdown-menu"
    class="dropdown-content"
    style="
      width: {dropdownWidth || 'auto'};
      top: {dropdownPosition.top}px;
      right: {dropdownPosition.left}px;
    "
    in:fade={{ duration: 100 }}
    out:fade={{ duration: 100 }}
  >
    <slot />
  </div>
{/if}

<style>
  .dropdown {
    display: inline-block;
  }

  .dropdown-content {
    position: absolute;
    padding: 12px 0;
    background-color: var(--black-3);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    border-radius: var(--radius-m);
    z-index: 1000;
    overflow: hidden;
  }
</style>
